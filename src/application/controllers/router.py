from fastapi import APIRouter
from src.application.controllers import (
    administrator, teacher, auth, form, 
    rating, reviews, lesson, schedule
)
api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(rating.router, prefix="/rating", tags=["rating"])
api_router.include_router(administrator.router, prefix="/admin", tags=["admin"])
api_router.include_router(teacher.router, prefix="/teacher", tags=["teacher"])
api_router.include_router(schedule.router, prefix="/schedule", tags=["schedule"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["reviews"])
api_router.include_router(lesson.router, prefix="/lesson", tags=["lesson"])
api_router.include_router(form.router, prefix="/form", tags=["form"])