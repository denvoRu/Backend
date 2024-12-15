from fastapi import APIRouter
from src.application.controllers import (
    administrator, teacher, auth, form, 
    reviews, schedule, module,
    institute, subject
)
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(administrator.router, prefix="/admin", tags=["admin"])
api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
api_router.include_router(institute.router, prefix="/institute", tags=["institute"])
api_router.include_router(module.router, prefix="/module", tags=["module"])
api_router.include_router(subject.router, prefix="/subject", tags=["subject"])
api_router.include_router(form.router, prefix="/form", tags=["form"])
api_router.include_router(reviews.router, prefix="/form", tags=["form"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])