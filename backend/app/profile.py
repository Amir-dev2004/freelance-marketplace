
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.auth import get_current_user
from app.models import User, UserProfile, Skill, UserSkill, PortfolioItem, Certificate
from app.schemas import (
    ProfileUpdateRequest,
    PortfolioCreateRequest,
    CertificateCreateRequest,
    PortfolioUpdateRequest,
    CertificateUpdateRequest
)
from datetime import datetime

router = APIRouter(tags=["Profile"])


# دریافت اطلاعات پروفایل کاربر
@router.get("/profile")
def get_profile(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user.id
    ).first()

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "address": user.address,
        "professional_title": profile.professional_title if profile else None,
        "bio": profile.bio if profile else None,
        "location": profile.location if profile else None
    }


# ویرایش اطلاعات حرفه‌ای پروفایل
@router.put("/profile")
def update_profile(
    data: ProfileUpdateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    profile = db.query(UserProfile).filter(
        UserProfile.user_id == user.id
    ).first()

    if not profile:
        profile = UserProfile(user_id=user.id)
        db.add(profile)

    profile.professional_title = data.professional_title
    profile.bio = data.bio
    profile.location = data.location

    db.commit()
    db.refresh(profile)

    return {
        "message": "Profile updated successfully",
        "professional_title": profile.professional_title,
        "bio": profile.bio,
        "location": profile.location
    }
# دریافت فهرست تمام مهارت‌های موجود
@router.get("/skills")
def get_all_skills(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skills = db.query(Skill).order_by(Skill.name).all()

    return [
        {
            "id": skill.id,
            "name": skill.name
        }
        for skill in skills
    ]


# دریافت مهارت‌های پروفایل کاربر
@router.get("/profile/skills")
def get_profile_skills(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skills = db.query(Skill).join(
        UserSkill,
        UserSkill.skill_id == Skill.id
    ).filter(
        UserSkill.user_id == user.id
    ).order_by(Skill.name).all()

    return [
        {
            "id": skill.id,
            "name": skill.name
        }
        for skill in skills
    ]


# افزودن مهارت به پروفایل کاربر
@router.post("/profile/skills/{skill_id}")
def add_profile_skill(
    skill_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    skill = db.query(Skill).filter(
        Skill.id == skill_id
    ).first()

    if not skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found"
        )

    existing = db.query(UserSkill).filter(
        UserSkill.user_id == user.id,
        UserSkill.skill_id == skill_id
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Skill already added"
        )

    user_skill = UserSkill(
        user_id=user.id,
        skill_id=skill_id
    )

    db.add(user_skill)
    db.commit()

    return {
        "message": "Skill added successfully",
        "skill": {
            "id": skill.id,
            "name": skill.name
        }
    }


# حذف مهارت از پروفایل کاربر
@router.delete("/profile/skills/{skill_id}")
def remove_profile_skill(
    skill_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user_skill = db.query(UserSkill).filter(
        UserSkill.user_id == user.id,
        UserSkill.skill_id == skill_id
    ).first()

    if not user_skill:
        raise HTTPException(
            status_code=404,
            detail="Skill not found in profile"
        )

    db.delete(user_skill)
    db.commit()

    return {
        "message": "Skill removed successfully"
    }
# دریافت نمونه‌کارهای کاربر
@router.get("/profile/portfolio")
def get_profile_portfolio(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    items = db.query(PortfolioItem).filter(
        PortfolioItem.user_id == user.id
    ).order_by(PortfolioItem.created_at.desc()).all()

    return [
        {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "url": item.url,
            "created_at": item.created_at
        }
        for item in items
    ]


# افزودن نمونه‌کار به پروفایل کاربر
@router.post("/profile/portfolio")
def add_profile_portfolio(
    data: PortfolioCreateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = PortfolioItem(
        user_id=user.id,
        title=data.title,
        description=data.description,
        url=data.url,
        created_at=datetime.utcnow()
    )

    db.add(item)
    db.commit()
    db.refresh(item)

    return {
        "message": "Portfolio item added successfully",
        "item": {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "url": item.url,
            "created_at": item.created_at
        }
    }
# ویرایش نمونه‌کار کاربر
@router.put("/profile/portfolio/{item_id}")
def update_profile_portfolio(
    item_id: int,
    data: PortfolioUpdateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(PortfolioItem).filter(
        PortfolioItem.id == item_id,
        PortfolioItem.user_id == user.id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Portfolio item not found"
        )

    item.title = data.title
    item.description = data.description
    item.url = data.url

    db.commit()
    db.refresh(item)

    return {
        "message": "Portfolio item updated successfully",
        "item": {
            "id": item.id,
            "title": item.title,
            "description": item.description,
            "url": item.url,
            "created_at": item.created_at
        }
    }

# حذف نمونه‌کار از پروفایل کاربر
@router.delete("/profile/portfolio/{item_id}")
def remove_profile_portfolio(
    item_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    item = db.query(PortfolioItem).filter(
        PortfolioItem.id == item_id,
        PortfolioItem.user_id == user.id
    ).first()

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Portfolio item not found"
        )

    db.delete(item)
    db.commit()

    return {
        "message": "Portfolio item removed successfully"
    }

# دریافت گواهینامه‌های کاربر
@router.get("/profile/certificates")
def get_profile_certificates(
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    certificates = db.query(Certificate).filter(
        Certificate.user_id == user.id
    ).order_by(Certificate.issue_date.desc()).all()

    return [
        {
            "id": certificate.id,
            "title": certificate.title,
            "issuer": certificate.issuer,
            "issue_date": certificate.issue_date,
            "certificate_url": certificate.certificate_url
        }
        for certificate in certificates
    ]


# افزودن گواهینامه به پروفایل کاربر
@router.post("/profile/certificates")
def add_profile_certificate(
    data: CertificateCreateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    certificate = Certificate(
        user_id=user.id,
        title=data.title,
        issuer=data.issuer,
        issue_date=data.issue_date,
        certificate_url=data.certificate_url
    )

    db.add(certificate)
    db.commit()
    db.refresh(certificate)

    return {
        "message": "Certificate added successfully",
        "certificate": {
            "id": certificate.id,
            "title": certificate.title,
            "issuer": certificate.issuer,
            "issue_date": certificate.issue_date,
            "certificate_url": certificate.certificate_url
        }
    }
# ویرایش گواهینامه کاربر
@router.put("/profile/certificates/{certificate_id}")
def update_profile_certificate(
    certificate_id: int,
    data: CertificateUpdateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id,
        Certificate.user_id == user.id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    certificate.title = data.title
    certificate.issuer = data.issuer
    certificate.issue_date = data.issue_date
    certificate.certificate_url = data.certificate_url

    db.commit()
    db.refresh(certificate)

    return {
        "message": "Certificate updated successfully",
        "certificate": {
            "id": certificate.id,
            "title": certificate.title,
            "issuer": certificate.issuer,
            "issue_date": certificate.issue_date,
            "certificate_url": certificate.certificate_url
        }
    }

# حذف گواهینامه از پروفایل کاربر
@router.delete("/profile/certificates/{certificate_id}")
def remove_profile_certificate(
    certificate_id: int,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    certificate = db.query(Certificate).filter(
        Certificate.id == certificate_id,
        Certificate.user_id == user.id
    ).first()

    if not certificate:
        raise HTTPException(
            status_code=404,
            detail="Certificate not found"
        )

    db.delete(certificate)
    db.commit()

    return {
        "message": "Certificate removed successfully"
    }