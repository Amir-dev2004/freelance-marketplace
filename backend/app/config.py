import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key")
    SESSION_COOKIE = "freelancer_session"
    SESSION_EXPIRE_HOURS = 12


settings = Settings()