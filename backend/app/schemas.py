
from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str
    
class SignupRequest(BaseModel):
    name: str
    phone: str | None = None
    address: str
    email: str
    codemeli: str
    password: str
    confirm_password: str
    roles: list[str]