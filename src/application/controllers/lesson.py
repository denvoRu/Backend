from src.domain.extensions.check_role import (
    CurrentTeacher, CurrentAdmin, CurrentUser
)
from src.domain.services import lesson_service

from fastapi import APIRouter, Query


router = APIRouter()


@router.get("/", description="Show all lessons")
async def get_my_lessons(
    teacher: CurrentTeacher, 
    start_date: str = Query(None, alias="start_date"),
    end_date: str = Query(None, alias="end_date"),
    filter = Query(None, alias="filter")
):
    return "Lessons are shown"


@router.get("/{teacher_id}", description="Show teacher lessons (for admins)")
async def get_lessons_of_teacher(
    admin: CurrentAdmin, 
    start_date: str = Query(None, alias="start_date"),
    end_date: str = Query(None, alias="end_date"),
    filter = Query(None, alias="filter")
):
    return "Lessons are shown"


@router.get("/{lesson_id}/members", description="Show members of lesson")
async def get__members_of_lesson(user: CurrentUser, lesson_id: int):
    return "Subject is shown"


@router.get("/{lesson_id}/statistics", description="Show statistics of lesson")
async def get_statistics_of_lesson(user: CurrentUser, lesson_id: int):
    return "Reviews are shown"
