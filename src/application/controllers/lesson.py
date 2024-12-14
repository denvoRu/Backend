from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/{lesson_id}", description="Show certain lesson")
async def show_lesson(admin: CurrentAdmin, lesson_id: int):
    return "Lesson is shown"

@router.patch("/{lesson_id}", description="Edit an existing lesson")
async def edit_lesson(admin: CurrentAdmin, lesson_id: int):
    return "Lesson is edited"


@router.get("/{lesson_id}/members", description="Show certain lesson")
async def show_lesson_members(admin: CurrentAdmin, lesson_id: int):
    return "Lesson is shown"


@router.get("/{lesson_id}/get_form_id", description="Return a form id")
async def get_form_id(admin: CurrentAdmin, lesson_id: int):
    return "Lesson is shown"
