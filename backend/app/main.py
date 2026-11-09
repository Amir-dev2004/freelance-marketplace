
from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.auth import router as auth_router

app = FastAPI(title="Freelancer Marketplace API")

app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SECRET_KEY,
    session_cookie=settings.SESSION_COOKIE,
    max_age=settings.SESSION_EXPIRE_HOURS * 60 * 60,
    same_site="lax",
    https_only=False,
)

app.include_router(auth_router)


@app.get("/")
def root():
    return {
        "message": "Freelancer Marketplace API is running"
    }
