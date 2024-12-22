from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin
from src.domain.services import lesson_service

from fastapi import APIRouter, Body, Query


router = APIRouter()


@router.get("/", description="Show all lessons")
async def get_lessons(
    teacher: CurrentTeacher, 
    start_date: str = "", 
    end_date: str = ""
):
    return "Lessons are shown"


@router.get("/{teacher_id}", description="Show all lessons")
async def get_lessons(
    admin: CurrentAdmin, 
    teacher_id: int, 
    start_date: str = "", 
    end_date: str = ""
):
    return "Lessons are shown"


@router.get("/{lesson_id}/members", description="Show certain subject")
async def get_lesson_members(admin: CurrentAdmin, lesson_id: int):
    return "Subject is shown"


@router.get("/{lesson_id}/get_form_id", description="Return a form id")
async def get_form_id(admin: CurrentAdmin, lesson_id: int):
    return "Subject is shown"
