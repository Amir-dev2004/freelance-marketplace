
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, UserRole, AdminAccount
from app.schemas import LoginRequest
from app.security import verify_password

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