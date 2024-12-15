from fastapi import APIRouter, Body, Query
from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin

router = APIRouter()

@router.get("/{lesson_id}/members", description="Show certain subject")
async def show_lesson_members(admin: CurrentAdmin, lesson_id: int):
    return "Subject is shown"


@router.get("/{lesson_id}/get_form_id", description="Return a form id")
async def get_form_id(admin: CurrentAdmin, lesson_id: int):
    return "Subject is shown"
