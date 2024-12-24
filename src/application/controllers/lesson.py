from src.domain.services import lesson_service
from src.domain.extensions.check_role import (
    CurrentTeacher, CurrentAdmin, CurrentUser
)

from fastapi import APIRouter
from datetime import date
from pydantic import UUID4


router = APIRouter()


@router.get("/", description="Show all lessons")
async def get_my_lessons(
    teacher: CurrentTeacher, 
    start_date: date,
    end_date: date,
):
    return await lesson_service.get_all(teacher.user_id, start_date, end_date)
    


@router.get("/{teacher_id}", description="Show teacher lessons (for admins)")
async def get_lessons_of_teacher(
    admin: CurrentAdmin, 
    teacher_id: UUID4,
    start_date: date,
    end_date: date,
):
    return await lesson_service.get_all(teacher_id, start_date, end_date)


@router.get("/{lesson_id}", description="Show lesson data if this lesson is active")
async def get_data_of_active_lesson(lesson_id: UUID4):
    return "Subject is shown"


@router.get("/{lesson_id}/members", description="Show members of lesson")
async def get__members_of_lesson(user: CurrentUser, lesson_id: UUID4):
    return "Subject is shown"


@router.get("/{lesson_id}/statistics", description="Show statistics of lesson")
async def get_statistics_of_lesson(user: CurrentUser, lesson_id: UUID4):
    return "Reviews are shown"
