
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