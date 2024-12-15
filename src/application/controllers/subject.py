from src.domain.extensions.check_role import CurrentAdmin, CurrentTeacher
from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/{subject_id}", description="Show certain subject")
async def show_lesson(admin: CurrentAdmin, subject_id: int):
    return "Lesson is shown"

@router.post("/", description="Create a new subject")
async def create_subject(teacher: CurrentTeacher):
    return "New subject is added"


@router.patch("/{subject_id}", description="Edit an existing subject")
async def edit_subject(admin: CurrentAdmin, subject_id: int):
    return "Subject is edited"


@router.get("/{subject_id}/members", description="Show certain subject")
async def show_lesson_members(admin: CurrentAdmin, subject_id: int):
    return "Subject is shown"


@router.get("/{subject_id}/get_form_id", description="Return a form id")
async def get_form_id(admin: CurrentAdmin, subject_id: int):
    return "Subject is shown"
