from fastapi import APIRouter
from src.app.api.routes import auth, moderation, teacher

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(moderation.router, prefix="/moderation", tags=["moderation"])
api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
