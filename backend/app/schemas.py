
import re
from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    email: str
    password: str

class SignupRequest(BaseModel):
    name: str = Field(min_length=2)
    phone: str | None = None
    address: str = Field(min_length=2)
    email: str
    codemeli: str
    password: str
    confirm_password: str
    roles: list[str] = Field(min_length=1)

    @field_validator("name", "address")
    @classmethod
    def validate_required_text(cls, value):
        if not value.strip():
            raise ValueError("این فیلد نمی‌تواند خالی باشد.")
        return value.strip()

    @field_validator("email")
    @classmethod
    def validate_email(cls, value):
        value = value.strip()

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)*\.com$"

        if not re.fullmatch(pattern, value):
            raise ValueError("ایمیل معتبر نیست.")

        return value

    @field_validator("codemeli")
    @classmethod
    def validate_codemeli(cls, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("کد ملی باید ۱۰ رقم باشد.")
        return value

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        if value is not None and value.strip():
            if not re.fullmatch(r"09\d{9}", value.strip()):
                raise ValueError("شماره تلفن معتبر نیست.")
            return value.strip()
        return None

    @field_validator("password", "confirm_password")
    @classmethod
    def validate_password_length(cls, value):
        if not value.strip():
            raise ValueError("رمز عبور نمی‌تواند خالی باشد.")
        if len(value) < 8:
            raise ValueError("رمز عبور باید حداقل ۸ کاراکتر باشد.")
        return value

class ForgotPasswordRequest(BaseModel):
    email: str


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str
    confirm_password: str

from datetime import date
from pydantic import BaseModel, Field, field_validator


class ProjectCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=50)
    description: str = Field(min_length=1)
    budget: int = Field(gt=0)
    pricing_type: str = "Fixed Price"
    status: str = "Draft"
    deadline: date | None = None
    category_ids: list[int] = []

    @field_validator("title", "description")
    @classmethod
    def validate_text(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("این فیلد نمی‌تواند خالی باشد.")
        return value

    @field_validator("pricing_type")
    @classmethod
    def validate_pricing_type(cls, value):
        if value not in ["Fixed Price", "Hourly"]:
            raise ValueError("نوع پرداخت نامعتبر است.")
        return value
    
    # اعتبارسنجی وضعیت پروژه
    @field_validator("status")
    @classmethod
    def validate_project_status(cls, value):
        if value not in ["Draft", "Open"]:
            raise ValueError("وضعیت پروژه نامعتبر است.")
        return value


    @field_validator("category_ids")
    @classmethod
    def validate_category_ids(cls, value):
        if any(category_id <= 0 for category_id in value):
            raise ValueError("شناسه دسته‌بندی نامعتبر است.")
        if len(value) != len(set(value)):
            raise ValueError("دسته‌بندی تکراری مجاز نیست.")
        return value


class ProjectUpdateRequest(ProjectCreateRequest):
    pass
class ProposalCreateRequest(BaseModel):
    cover_letter: str = Field(min_length=1)
    budget: int = Field(gt=0)
    estimated_duration_days: int = Field(gt=0)

    @field_validator("cover_letter")
    @classmethod
    def validate_cover_letter(cls, value):
        value = value.strip()
        if not value:
            raise ValueError("متن پیشنهاد نمی‌تواند خالی باشد.")
        return value

class ProfileUpdateRequest(BaseModel):
    professional_title: str | None = Field(default=None, max_length=100)
    bio: str | None = Field(default=None, max_length=1000)
    location: str | None = Field(default=None, max_length=150)

    @field_validator(
        "professional_title",
        "bio",
        "location"
    )
    @classmethod
    def validate_profile_text(cls, value):
        if value is None:
            return None

        value = value.strip()
        return value if value else None

class PortfolioCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    description: str | None = Field(default=None, max_length=1000)
    url: str | None = Field(default=None, max_length=500)

    @field_validator("title", "description", "url")
    @classmethod
    def validate_portfolio_text(cls, value):
        if value is None:
            return None

        value = value.strip()
        return value if value else None

class CertificateCreateRequest(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    issuer: str | None = Field(default=None, max_length=150)
    issue_date: date | None = None
    certificate_url: str | None = Field(default=None, max_length=500)

    @field_validator("title", "issuer", "certificate_url")
    @classmethod
    def validate_certificate_text(cls, value):
        if value is None:
            return None

        value = value.strip()
        return value if value else None

class PortfolioUpdateRequest(PortfolioCreateRequest):
    pass


class CertificateUpdateRequest(CertificateCreateRequest):
    pass