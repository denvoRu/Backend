from fastapi import APIRouter
from application.controllers import (
    administrator, teacher, auth, form
)
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(administrator.router, prefix="/admin", tags=["admin"])
api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
api_router.include_router(form.router, prefix="/form", tags=["form"])
