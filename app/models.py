
from sqlalchemy import (
    Column,
    Integer,
    String,
    Unicode,
    DateTime,
    Date,
    ForeignKey,
    func
)

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(50), nullable=False)
    phone = Column(String(50), nullable=True)
    address = Column(Unicode(250), nullable=False)
    email = Column(String(100), nullable=False)
    codemeli = Column(String(20), nullable=False)
    password_hash = Column("PasswordHash", Unicode(255), nullable=False)

    account_status = Column(
        "AccountStatus", String(10), nullable=False,
        server_default="Active"
    )
    created_at = Column(
        "CreatedAt", DateTime, nullable=False,
        server_default=func.getutcdate()
    )
    updated_at = Column(
        "UpdatedAt", DateTime, nullable=False,
        server_default=func.sysdatetime()
    )


class UserRole(Base):
    __tablename__ = "UserRoles"

    user_id = Column("UserId", Integer, ForeignKey("user.id"), primary_key=True)
    role = Column(String(20), primary_key=True)


class AdminAccount(Base):
    __tablename__ = "AdminAccounts"

    user_id = Column("UserId", Integer, ForeignKey("user.id"), primary_key=True)
    granted_at = Column("GrantedAt", DateTime, nullable=False)


class PasswordResetToken(Base):
    __tablename__ = "PasswordResetTokens"

    id = Column("Id", Integer, primary_key=True)
    user_id = Column("UserId", Integer, ForeignKey("user.id"), nullable=False)
    token_hash = Column("TokenHash", String(64), nullable=False, unique=True)
    expires_at = Column("ExpiresAt", DateTime, nullable=False)
    used_at = Column("UsedAt", DateTime, nullable=True)
    created_at = Column(
        "CreatedAt", DateTime, nullable=False,
        server_default=func.sysdatetime()
    )


class Category(Base):
    __tablename__ = "Categories"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    title = Column("Title", Unicode(100), nullable=False)


class Skill(Base):
    __tablename__ = "Skills"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    name = Column("Name", Unicode(100), nullable=False)


class UserProfile(Base):
    __tablename__ = "UserProfiles"

    user_id = Column(
        "UserId", Integer, ForeignKey("user.id"), primary_key=True
    )
    professional_title = Column("ProfessionalTitle", Unicode(100), nullable=True)
    bio = Column("Bio", Unicode(1000), nullable=True)
    location = Column("Location", Unicode(150), nullable=True)


class UserSkill(Base):
    __tablename__ = "UserSkills"

    user_id = Column(
        "UserId", Integer, ForeignKey("user.id"), primary_key=True
    )
    skill_id = Column(
        "SkillId", Integer, ForeignKey("Skills.Id"), primary_key=True
    )


class Certificate(Base):
    __tablename__ = "Certificates"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("UserId", Integer, ForeignKey("user.id"), nullable=False)
    title = Column("Title", Unicode(150), nullable=False)
    issuer = Column("Issuer", Unicode(150), nullable=True)
    issue_date = Column("IssueDate", Date, nullable=True)
    certificate_url = Column("CertificateUrl", Unicode(500), nullable=True)


class PortfolioItem(Base):
    __tablename__ = "PortfolioItems"

    id = Column("Id", Integer, primary_key=True, autoincrement=True)
    user_id = Column("UserId", Integer, ForeignKey("user.id"), nullable=False)
    title = Column("Title", Unicode(150), nullable=False)
    description = Column("Description", Unicode(1000), nullable=True)
    url = Column("Url", Unicode(500), nullable=True)
    created_at = Column("CreatedAt", DateTime, nullable=False)


class Project(Base):
    __tablename__ = "project"
    __table_args__ = {"implicit_returning": False}

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(Unicode(50), nullable=False)
    description = Column(Unicode, nullable=False)
    budget = Column(Integer, nullable=False)

    client_id = Column(
        "client-id", Integer, ForeignKey("user.id"), nullable=False
    )

    pricing_type = Column("PricingType", String(20), nullable=False)
    project_status = Column("ProjectStatus", String(20), nullable=False)
    created_at = Column("CreatedAt", DateTime, nullable=False, server_default=func.sysdatetime())
    updated_at = Column("UpdatedAt", DateTime, nullable=False, server_default=func.sysdatetime())
    deadline = Column("Deadline", Date, nullable=True)


class ProjectCategory(Base):
    __tablename__ = "ProjectCategories"

    project_id = Column(
        "ProjectId", Integer, ForeignKey("project.id"), primary_key=True
    )
    category_id = Column(
        "CategoryId", Integer, ForeignKey("Categories.Id"), primary_key=True
    )


class ProjectSkill(Base):
    __tablename__ = "ProjectSkills"

    project_id = Column(
        "ProjectId", Integer, ForeignKey("project.id"), primary_key=True
    )
    skill_id = Column(
        "SkillId", Integer, ForeignKey("Skills.Id"), primary_key=True
    )


class Proposal(Base):
    __tablename__ = "proposal"
    __table_args__ = {"implicit_returning": False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    cover_letter = Column("cover-letter", Unicode, nullable=False)

    estimated_duration_days = Column(
        "EstimatedDurationDays", Integer, nullable=False
    )

    freelancer_id = Column(
        "freelancer-id", Integer, ForeignKey("user.id"), nullable=False
    )
    project_id = Column(
        "project-id", Integer, ForeignKey("project.id"), nullable=False
    )

    budget = Column(Integer, nullable=False)
    status = Column("status", String(20), nullable=False)
    created_at = Column(
    "CreatedAt",
    DateTime,
    nullable=False,
    server_default=func.sysdatetime()
)
