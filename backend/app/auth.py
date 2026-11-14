from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserRole, AdminAccount, PasswordResetToken
from app.schemas import (
    LoginRequest,
    SignupRequest,
    ForgotPasswordRequest,
    ResetPasswordRequest
)
from app.security import (
    verify_password,
    hash_password,
    generate_reset_token,
    hash_reset_token
)
from collections import defaultdict, deque
from threading import Lock
import time
router = APIRouter()

# Login rate limit settings
MAX_LOGIN_ATTEMPTS = 5
LOGIN_WINDOW_SECONDS = 300
LOGIN_BLOCK_SECONDS = 300

login_attempts = defaultdict(deque)
login_blocked_until = {}
login_rate_limit_lock = Lock()


def get_client_ip(request: Request):
    if request.client:
        return request.client.host
    return "unknown"


def check_login_rate_limit(ip: str):
    now = time.monotonic()

    with login_rate_limit_lock:
        blocked_until = login_blocked_until.get(ip, 0)

        if now < blocked_until:
            remaining = int(blocked_until - now) + 1
            raise HTTPException(
                status_code=429,
                detail=f"Too Many Requests. Try again in {remaining} seconds."
            )

        attempts = login_attempts[ip]

        while attempts and now - attempts[0] >= LOGIN_WINDOW_SECONDS:
            attempts.popleft()


def record_failed_login(ip: str):
    now = time.monotonic()

    with login_rate_limit_lock:
        attempts = login_attempts[ip]

        while attempts and now - attempts[0] >= LOGIN_WINDOW_SECONDS:
            attempts.popleft()

        attempts.append(now)

        if len(attempts) >= MAX_LOGIN_ATTEMPTS:
            login_blocked_until[ip] = now + LOGIN_BLOCK_SECONDS
            attempts.clear()


def clear_login_attempts(ip: str):
    with login_rate_limit_lock:
        login_attempts.pop(ip, None)
        login_blocked_until.pop(ip, None)

@router.post("/login")
def login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
    ip = get_client_ip(request)

    # Check rate limit before processing login
    check_login_rate_limit(ip)

    user = db.query(User).filter(User.email == data.email).first()

    # Record failed login attempt
    if not user or not verify_password(data.password, user.password_hash):
        record_failed_login(ip)

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    # Clear failed attempts after correct credentials
    clear_login_attempts(ip)

    if user.account_status.lower() != "active":
        raise HTTPException(
            status_code=403,
            detail="Your account is not active"
        )

    roles = [
        role.role
        for role in db.query(UserRole).filter(
            UserRole.user_id == user.id
        ).all()
    ]

    is_admin = db.query(AdminAccount).filter(
        AdminAccount.user_id == user.id
    ).first()

    if is_admin:
        roles.append("Admin")

    request.session.clear()
    request.session["user_id"] = user.id

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        },
        "roles": roles
    }
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if user.account_status.lower() != "active":
        raise HTTPException(
            status_code=403,
            detail="Your account is not active"
        )

    roles = [
        role.role
        for role in db.query(UserRole).filter(
            UserRole.user_id == user.id
        ).all()
    ]

    is_admin = db.query(AdminAccount).filter(
        AdminAccount.user_id == user.id
    ).first()

    if is_admin:
        roles.append("Admin")

    request.session.clear()
    request.session["user_id"] = user.id

    return {
        "message": "Login successful",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        },
        "roles": roles
    }


# بررسی احراز هویت کاربر
def get_current_user(
    request: Request,
    db: Session = Depends(get_db)
):
    user_id = request.session.get("user_id")

    if not user_id:
        raise HTTPException(
            status_code=401,
            detail="Not authenticated"
        )

    user = db.query(User).filter(User.id == user_id).first()

    if not user:
        request.session.clear()
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    if user.account_status.lower() != "active":
        request.session.clear()
        raise HTTPException(
            status_code=403,
            detail="Your account is not active"
        )

    return user


# بررسی دسترسی کاربر بر اساس نقش
def require_role(required_role: str):
    def role_checker(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        if required_role == "Admin":
            has_role = db.query(AdminAccount).filter(
                AdminAccount.user_id == user.id
            ).first()
        else:
            has_role = db.query(UserRole).filter(
                UserRole.user_id == user.id,
                UserRole.role == required_role
            ).first()

        if not has_role:
            raise HTTPException(
                status_code=403,
                detail="You don't have permission to access this resource"
            )

        return user

    return role_checker


# دریافت اطلاعات کاربر فعلی
@router.get("/me")
def me(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    roles = [
        role.role
        for role in db.query(UserRole).filter(
            UserRole.user_id == user.id
        ).all()
    ]

    is_admin = db.query(AdminAccount).filter(
        AdminAccount.user_id == user.id
    ).first()

    if is_admin:
        roles.append("Admin")

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "roles": roles
    }


@router.post("/logout")
def logout(request: Request):
    request.session.clear()

    return {
        "message": "Logout successful"
    }
@router.get("/admin-test")
def admin_test(
    user: User = Depends(require_role("Admin"))
):
    return {
        "message": "Welcome Admin",
        "user": user.name
    }
@router.post("/signup")
def signup(
    data: SignupRequest,
    db: Session = Depends(get_db)
):
    # بررسی تطابق رمز عبور
    if data.password != data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="رمزهای عبور مطابقت ندارند."
        )

    # بررسی نقش‌های انتخاب‌شده
    allowed_roles = {"Client", "Freelancer"}

    if not data.roles or not set(data.roles).issubset(allowed_roles):
        raise HTTPException(
            status_code=400,
            detail="نقش انتخاب‌شده معتبر نیست."
        )

    # بررسی تکراری بودن حساب
    existing_user = db.query(User).filter(
        (User.email == data.email) |
        (User.codemeli == data.codemeli)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="این حساب از قبل وجود دارد."
        )

    # ساخت کاربر جدید
    new_user = User(
        name=data.name,
        phone=data.phone,
        address=data.address,
        email=data.email,
        codemeli=data.codemeli,
        password_hash=hash_password(data.password)
    )

    try:
        db.add(new_user)
        db.flush()

        # ذخیره نقش‌های کاربر
        for role in set(data.roles):
            db.add(UserRole(
                user_id=new_user.id,
                role=role
            ))

        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="این حساب از قبل وجود دارد."
        )

    return {
        "message": "Registration successful",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        },
        "roles": list(set(data.roles))
    }

@router.post("/forgot-password")
def forgot_password(
    data: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == data.email
    ).first()

    # پیام یکسان برای جلوگیری از افشای وجود ایمیل
    response = {
        "message": "If the email exists, a reset link has been generated."
    }

    if not user:
        return response

    # ساخت توکن تصادفی
    token = generate_reset_token()

    # ذخیره هش توکن در دیتابیس
    reset_record = PasswordResetToken(
        user_id=user.id,
        token_hash=hash_reset_token(token),
        expires_at=datetime.utcnow() + timedelta(minutes=15)
    )

    db.add(reset_record)
    db.commit()

    # نمایش لینک در ترمینال برای محیط توسعه
    reset_link = f"http://127.0.0.1:5500/frontend/reset-password.html?token={token}"
    print(f"Password reset link: {reset_link}")

    return response

@router.post("/reset-password")
def reset_password(
    data: ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    # بررسی تطابق رمزهای عبور
    if data.new_password != data.confirm_password:
        raise HTTPException(
            status_code=400,
            detail="Passwords do not match"
        )

    # پیدا کردن توکن معتبر
    reset_record = db.query(PasswordResetToken).filter(
        PasswordResetToken.token_hash == hash_reset_token(data.token),
        PasswordResetToken.used_at.is_(None),
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()

    if not reset_record:
        raise HTTPException(
            status_code=400,
            detail="Invalid or expired reset token"
        )

    # پیدا کردن کاربر
    user = db.query(User).filter(
        User.id == reset_record.user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=400,
            detail="Invalid reset token"
        )

    # تغییر رمز عبور
    user.password_hash = hash_password(data.new_password)

    # یک‌بارمصرف کردن توکن
    reset_record.used_at = datetime.utcnow()

    db.commit()

    return {
        "message": "Password reset successful"
    }