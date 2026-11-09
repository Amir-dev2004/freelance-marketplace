from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserRole, AdminAccount
from app.schemas import LoginRequest, SignupRequest
from app.security import verify_password, hash_password
router = APIRouter()


@router.post("/login")
def login(
    data: LoginRequest,
    request: Request,
    db: Session = Depends(get_db)
):
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
            detail="Passwords do not match"
        )

    # بررسی نقش‌های انتخاب‌شده
    allowed_roles = {"Client", "Freelancer"}

    if not data.roles or not set(data.roles).issubset(allowed_roles):
        raise HTTPException(
            status_code=400,
            detail="Invalid roles"
        )

    # بررسی تکراری نبودن ایمیل
    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="Email already registered"
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

    return {
        "message": "Registration successful",
        "user": {
            "id": new_user.id,
            "name": new_user.name,
            "email": new_user.email
        },
        "roles": list(set(data.roles))
    }