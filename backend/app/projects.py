from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, func

from app.database import get_db
from app.auth import get_current_user, require_role
from app.models import (
    Category,
    Project,
    ProjectCategory,
    ProjectSkill,
    Proposal,
    User,
    UserProfile,
    UserSkill,
    Skill
)
from app.schemas import (
    ProjectCreateRequest,
    ProjectUpdateRequest,
    ProposalCreateRequest
)
router = APIRouter(tags=["Projects"])


@router.get("/categories")
def get_categories(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    categories = db.query(Category).order_by(Category.title.asc()).all()

    return [
        {
            "id": category.id,
            "title": category.title
        }
        for category in categories
    ]


@router.get("/projects")
def get_projects(
    category_id: int | None = Query(default=None, gt=0),
    search: str | None = None,
    pricing_type: str | None = None,
    min_budget: int | None = Query(default=None, ge=0),
    max_budget: int | None = Query(default=None, ge=0),
    sort: str = "newest",
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = (
        db.query(Project, User.name.label("client_name"))
        .join(User, Project.client_id == User.id)
        .filter(Project.project_status == "Open")
    )

    if category_id is not None:
        category_exists = db.query(ProjectCategory).filter(
            ProjectCategory.project_id == Project.id,
            ProjectCategory.category_id == category_id
        ).exists()

        query = query.filter(category_exists)

    if search and search.strip():
        search_term = f"%{search.strip()}%"
        query = query.filter(
            (Project.title.ilike(search_term)) |
            (Project.description.ilike(search_term))
        )

    if pricing_type:
        if pricing_type not in ["Fixed Price", "Hourly"]:
            raise HTTPException(
                status_code=400,
                detail="Invalid pricing type"
            )

        query = query.filter(Project.pricing_type == pricing_type)

    if min_budget is not None and max_budget is not None:
        if min_budget > max_budget:
            raise HTTPException(
                status_code=400,
                detail="Minimum budget cannot exceed maximum budget"
            )

    if min_budget is not None:
        query = query.filter(Project.budget >= min_budget)

    if max_budget is not None:
        query = query.filter(Project.budget <= max_budget)

    if sort == "newest":
        query = query.order_by(desc(Project.created_at))
    elif sort == "cheapest":
        query = query.order_by(asc(Project.budget))
    elif sort == "expensive":
        query = query.order_by(desc(Project.budget))
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort option"
        )

    total = query.count()

    results = (
        query
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    projects = [
        {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "budget": project.budget,
            "pricing_type": project.pricing_type,
            "created_at": project.created_at,
            "deadline": project.deadline,
            "client_name": client_name
        }
        for project, client_name in results
    ]

    return {
        "items": projects,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

@router.get("/my-projects")
def get_my_projects(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    proposal_count = (
        db.query(func.count(Proposal.id))
        .filter(Proposal.project_id == Project.id)
        .correlate(Project)
        .scalar_subquery()
    )

    query = db.query(
        Project,
        proposal_count.label("proposal_count")
    ).filter(
        Project.client_id == user.id
    )

    total = query.count()

    results = (
        query
        .order_by(desc(Project.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    projects = [
        {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "budget": project.budget,
            "pricing_type": project.pricing_type,
            "status": project.project_status,
            "created_at": project.created_at,
            "deadline": project.deadline,
            "proposal_count": count
        }
        for project, count in results
    ]

    return {
        "items": projects,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

@router.post("/projects")
def create_project(
    project_data: ProjectCreateRequest,
    user=Depends(require_role("Client")),
    db: Session = Depends(get_db)
):
    # بررسی دسته‌بندی‌های انتخاب‌شده
    if project_data.category_ids:
        categories = db.query(Category).filter(
            Category.id.in_(project_data.category_ids)
        ).all()

        if len(categories) != len(project_data.category_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more categories do not exist"
            )

    # ایجاد پروژه با وضعیت پیش‌نویس
    new_project = Project(
        title=project_data.title,
        description=project_data.description,
        budget=project_data.budget,
        client_id=user.id,
        pricing_type=project_data.pricing_type,
        project_status=project_data.status,
        deadline=project_data.deadline
    )

    db.add(new_project)
    db.flush()

    # ثبت دسته‌بندی‌های پروژه
    for category_id in project_data.category_ids:
        db.add(
            ProjectCategory(
                project_id=new_project.id,
                category_id=category_id
            )
        )

    db.commit()
    db.refresh(new_project)

    return {
        "message": "Project created successfully",
        "project": {
            "id": new_project.id,
            "title": new_project.title,
            "description": new_project.description,
            "budget": new_project.budget,
            "pricing_type": new_project.pricing_type,
            "status": new_project.project_status,
            "deadline": new_project.deadline
        }
    }
@router.put("/projects/{project_id}")
def update_project(
    project_id: int,
    project_data: ProjectUpdateRequest,
    user=Depends(require_role("Client")),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if project.client_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to edit this project"
        )

    if project.project_status not in ["Draft", "Open"]:
        raise HTTPException(
            status_code=400,
            detail="This project cannot be edited in its current status"
        )

    # بررسی دسته‌بندی‌ها
    if project_data.category_ids:
        categories = db.query(Category).filter(
            Category.id.in_(project_data.category_ids)
        ).all()

        if len(categories) != len(project_data.category_ids):
            raise HTTPException(
                status_code=400,
                detail="One or more categories do not exist"
            )

    # به‌روزرسانی اطلاعات پروژه
    project.title = project_data.title
    project.description = project_data.description
    project.budget = project_data.budget
    project.pricing_type = project_data.pricing_type
    project.deadline = project_data.deadline

    # جایگزینی دسته‌بندی‌های قبلی
    db.query(ProjectCategory).filter(
        ProjectCategory.project_id == project.id
    ).delete(synchronize_session=False)

    for category_id in project_data.category_ids:
        db.add(
            ProjectCategory(
                project_id=project.id,
                category_id=category_id
            )
        )

    db.commit()
    db.refresh(project)

    return {
        "message": "Project updated successfully",
        "project": {
            "id": project.id,
            "title": project.title,
            "description": project.description,
            "budget": project.budget,
            "pricing_type": project.pricing_type,
            "status": project.project_status,
            "deadline": project.deadline
        }
    }

@router.patch("/projects/{project_id}/publish")
def publish_project(
    project_id: int,
    user=Depends(require_role("Client")),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if project.client_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to publish this project"
        )

    if project.project_status != "Draft":
        raise HTTPException(
            status_code=400,
            detail="Only draft projects can be published"
        )

    project.project_status = "Open"

    db.commit()
    db.refresh(project)

    return {
        "message": "Project published successfully",
        "project": {
            "id": project.id,
            "title": project.title,
            "status": project.project_status
        }
    }
@router.delete("/projects/{project_id}")
def delete_project(
    project_id: int,
    user=Depends(require_role("Client")),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if project.client_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to delete this project"
        )

    if project.project_status not in ["Draft", "Open"]:
        raise HTTPException(
            status_code=400,
            detail="This project cannot be deleted in its current status"
        )

    # جلوگیری از حذف پروژه دارای پیشنهاد
    has_proposals = db.query(Proposal.id).filter(
        Proposal.project_id == project_id
    ).first()

    if has_proposals:
        raise HTTPException(
            status_code=400,
            detail="Projects with proposals cannot be deleted"
        )

    # حذف ارتباطات پروژه
    db.query(ProjectCategory).filter(
        ProjectCategory.project_id == project_id
    ).delete(synchronize_session=False)

    db.query(ProjectSkill).filter(
        ProjectSkill.project_id == project_id
    ).delete(synchronize_session=False)

    db.delete(project)
    db.commit()

    return {
        "message": "Project deleted successfully",
        "project_id": project_id
    }
@router.get("/projects/{project_id}")
def get_project_details(
    project_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    # پروژه‌های غیرعمومی فقط برای صاحب پروژه یا فریلنسری که پیشنهاد داده قابل مشاهده‌اند
    has_proposal = db.query(Proposal.id).filter(
        Proposal.project_id == project.id,
        Proposal.freelancer_id == user.id
    ).first() is not None

    if (
        project.project_status != "Open"
        and project.client_id != user.id
        and not has_proposal
    ):
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )


    client = db.query(User).filter(
        User.id == project.client_id
    ).first()

    categories = (
        db.query(Category)
        .join(
            ProjectCategory,
            Category.id == ProjectCategory.category_id
        )
        .filter(ProjectCategory.project_id == project.id)
        .all()
    )
    existing_proposal = db.query(Proposal).filter(
        Proposal.freelancer_id == user.id,
        Proposal.project_id == project.id
    ).first()
    return {
        "id": project.id,
        "title": project.title,
        "description": project.description,
        "budget": project.budget,
        "pricing_type": project.pricing_type,
        "status": project.project_status,
        "has_submitted_proposal": existing_proposal is not None,
        "my_proposal": {
    "id": existing_proposal.id,
    "cover_letter": existing_proposal.cover_letter,
    "budget": existing_proposal.budget,
    "estimated_duration_days": existing_proposal.estimated_duration_days,
    "status": existing_proposal.status,
    "created_at": existing_proposal.created_at
} if existing_proposal else None,
        "created_at": project.created_at,
        "deadline": project.deadline,
        "client": {
            "id": client.id,
            "name": client.name
        },
        "categories": [
            {
                "id": category.id,
                "title": category.title
            }
            for category in categories
        ]
    }

@router.get("/projects/{project_id}/proposals")
def get_project_proposals(
    project_id: int,
    user=Depends(require_role("Client")),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    if project.client_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to view these proposals"
        )

    proposals = (
        db.query(Proposal, User)
        .join(User, Proposal.freelancer_id == User.id)
        .filter(Proposal.project_id == project_id)
        .order_by(desc(Proposal.created_at))
        .all()
    )

    results = []

    for proposal, freelancer in proposals:
        profile = db.query(UserProfile).filter(
            UserProfile.user_id == freelancer.id
        ).first()

        skills = (
            db.query(Skill)
            .join(UserSkill, Skill.id == UserSkill.skill_id)
            .filter(UserSkill.user_id == freelancer.id)
            .all()
        )

        results.append({
            "id": proposal.id,
            "cover_letter": proposal.cover_letter,
            "budget": proposal.budget,
            "estimated_duration_days": proposal.estimated_duration_days,
            "status": proposal.status,
            "created_at": proposal.created_at,
            "freelancer": {
                "id": freelancer.id,
                "name": freelancer.name,
                "professional_title": (
                    profile.professional_title if profile else None
                ),
                "bio": profile.bio if profile else None,
                "skills": [
                    skill.name for skill in skills
                ]
            }
        })

    return {
        "project_id": project_id,
        "project_title": project.title,
        "total": len(results),
        "items": results
    }

@router.post("/projects/{project_id}/proposals")
def create_proposal(
    project_id: int,
    proposal_data: ProposalCreateRequest,
    user=Depends(require_role("Freelancer")),
    db: Session = Depends(get_db)
):
    # بررسی وجود پروژه
    project = db.query(Project).filter(
        Project.id == project_id
    ).first()

    if not project:
        raise HTTPException(
            status_code=404,
            detail="Project not found"
        )

    # فقط پروژه‌های منتشرشده قابل پیشنهاد هستند
    if project.project_status != "Open":
        raise HTTPException(
            status_code=400,
            detail="You can only apply to open projects"
        )

    # جلوگیری از پیشنهاد برای پروژه خود فریلنسر
    if project.client_id == user.id:
        raise HTTPException(
            status_code=400,
            detail="You cannot apply to your own project"
        )

    # بررسی پیشنهاد تکراری
    existing_proposal = db.query(Proposal).filter(
        Proposal.freelancer_id == user.id,
        Proposal.project_id == project_id
    ).first()

    if existing_proposal:
        raise HTTPException(
            status_code=400,
            detail="You have already submitted a proposal for this project"
        )

    # ایجاد پیشنهاد
    new_proposal = Proposal(
        cover_letter=proposal_data.cover_letter,
        budget=proposal_data.budget,
        estimated_duration_days=proposal_data.estimated_duration_days,
        freelancer_id=user.id,
        project_id=project_id,
        status="Pending"
    )

    db.add(new_proposal)
    db.commit()
    db.refresh(new_proposal)

    return {
        "message": "Proposal submitted successfully",
        "proposal": {
            "id": new_proposal.id,
            "project_id": new_proposal.project_id,
            "budget": new_proposal.budget,
            "estimated_duration_days": new_proposal.estimated_duration_days,
            "status": new_proposal.status,
            "created_at": new_proposal.created_at
        }
    }

@router.get("/my-proposals")
def get_my_proposals(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=10, ge=1, le=50),
    user=Depends(require_role("Freelancer")),
    db: Session = Depends(get_db)
):
    query = (
        db.query(Proposal, Project)
        .join(Project, Proposal.project_id == Project.id)
        .filter(Proposal.freelancer_id == user.id)
    )

    total = query.count()

    results = (
        query
        .order_by(desc(Proposal.created_at))
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    proposals = [
        {
            "id": proposal.id,
            "project": {
                "id": project.id,
                "title": project.title
            },
            "budget": proposal.budget,
            "cover_letter": proposal.cover_letter,
            "estimated_duration_days": proposal.estimated_duration_days,
            "status": proposal.status,
            "created_at": proposal.created_at
        }
        for proposal, project in results
    ]

    return {
        "items": proposals,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }

@router.patch("/proposals/{proposal_id}/withdraw")
def withdraw_proposal(
    proposal_id: int,
    user=Depends(require_role("Freelancer")),
    db: Session = Depends(get_db)
):
    proposal = db.query(Proposal).filter(
        Proposal.id == proposal_id
    ).first()

    if not proposal:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found"
        )

    # فقط صاحب پیشنهاد اجازه انصراف دارد
    if proposal.freelancer_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to withdraw this proposal"
        )

    # فقط پیشنهادهای در انتظار قابل انصراف هستند
    if proposal.status != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending proposals can be withdrawn"
        )

    proposal.status = "Withdrawn"

    db.commit()
    db.refresh(proposal)

    return {
        "message": "Proposal withdrawn successfully",
        "proposal": {
            "id": proposal.id,
            "status": proposal.status
        }
    }


@router.patch("/proposals/{proposal_id}/accept")
def accept_proposal(
    proposal_id: int,
    user=Depends(require_role("Client")),
    db: Session = Depends(get_db)
):
    proposal = db.query(Proposal).filter(
        Proposal.id == proposal_id
    ).first()

    if not proposal:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found"
        )

    project = db.query(Project).filter(
        Project.id == proposal.project_id
    ).first()

    if project.client_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to accept this proposal"
        )

    if proposal.status != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending proposals can be accepted"
        )

    if project.project_status != "Open":
        raise HTTPException(
            status_code=400,
            detail="This project is not open"
        )

    try:
        # رد کردن سایر پیشنهادهای در انتظار
        other_proposals = db.query(Proposal).filter(
            Proposal.project_id == project.id,
            Proposal.id != proposal.id,
            Proposal.status == "Pending"
        ).all()

        for other in other_proposals:
            other.status = "Rejected"

        # قبول پیشنهاد انتخاب‌شده
        proposal.status = "Accepted"

        # تغییر وضعیت پروژه
        project.project_status = "In Progress"

        db.commit()

    except Exception:
        db.rollback()
        raise

    db.refresh(proposal)
    db.refresh(project)

    return {
        "message": "Proposal accepted successfully",
        "proposal_id": proposal.id,
        "proposal_status": proposal.status,
        "project_status": project.project_status
    }


@router.patch("/proposals/{proposal_id}/reject")
def reject_proposal(
    proposal_id: int,
    user=Depends(require_role("Client")),
    db: Session = Depends(get_db)
):
    proposal = db.query(Proposal).filter(
        Proposal.id == proposal_id
    ).first()

    if not proposal:
        raise HTTPException(
            status_code=404,
            detail="Proposal not found"
        )

    project = db.query(Project).filter(
        Project.id == proposal.project_id
    ).first()

    if project.client_id != user.id:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to reject this proposal"
        )

    if proposal.status != "Pending":
        raise HTTPException(
            status_code=400,
            detail="Only pending proposals can be rejected"
        )

    proposal.status = "Rejected"

    db.commit()
    db.refresh(proposal)

    return {
        "message": "Proposal rejected successfully",
        "proposal_id": proposal.id,
        "proposal_status": proposal.status
    }
