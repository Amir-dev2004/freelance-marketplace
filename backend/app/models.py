from sqlalchemy import (
    Column,
    Integer,
    String,
    Unicode,
    DateTime,
    ForeignKey,
    func
)

from app.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(Unicode(100), nullable=False)
    phone = Column(String(50), nullable=True)
    address = Column(Unicode(500), nullable=False)
    email = Column(String(100), nullable=False)
    codemeli = Column(String(20), nullable=False)

    password_hash = Column("PasswordHash", Unicode(255), nullable=False)

    account_status = Column(
        "AccountStatus",
        String(10),
        nullable=False,
        server_default="Active"
    )

    created_at = Column(
        "CreatedAt",
        DateTime,
        nullable=False,
        server_default=func.sysdatetime()
    )

    updated_at = Column(
        "UpdatedAt",
        DateTime,
        nullable=False,
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