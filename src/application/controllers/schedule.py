from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin
from fastapi import APIRouter

router = APIRouter()

@router.get("/", description="Show all lessons")
async def show_lessons(teacher: CurrentTeacher):
    return "Lessons are shown"

@router.get("/{teacher_id}", description="Show all lessons (for admins)")
async def show_lessons(admin: CurrentAdmin, teacher_id: int):
    return "Lessons are shown"
