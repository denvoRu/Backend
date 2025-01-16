from fastapi import APIRouter
from src.application.controllers import (
    administrator, teacher, auth,
    schedule, module, institute, 
    subject, lesson, feedback,
    university, const_link
)


api_router = APIRouter()


api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(administrator.router, prefix="/admin", tags=["admin"])
api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
api_router.include_router(university.router, prefix="/university", tags=["university"])
api_router.include_router(institute.router, prefix="/institute", tags=["institute"])
api_router.include_router(module.router, prefix="/module", tags=["module"])
api_router.include_router(subject.router, prefix="/subject", tags=["subject"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(const_link.router, prefix="/const_link", tags=["const_link"])
api_router.include_router(lesson.router, prefix="/lesson", tags=["lesson"])
api_router.include_router(feedback.router, prefix="/lesson", tags=["lesson"])
