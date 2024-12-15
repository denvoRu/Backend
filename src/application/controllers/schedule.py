from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin
from fastapi import APIRouter

router = APIRouter()

@router.get("/lessons", description="Show all lessons")
async def show_lessons(teacher: CurrentTeacher):
    return "Lessons are shown"

@router.get("/{teacher_id}/lessons", description="Show all lessons")
async def show_lessons(admin: CurrentAdmin):
    return "Lessons are shown"

@router.get("/lessons/{lesson_id}", description="Show certain lesson")
async def show_lesson(teacher: CurrentTeacher, lesson_id: int):
    return "Lesson is shown"


@router.get("/{teacher_id}/lessons/{lesson_id}", description="Show certain lesson")
async def show_lesson_teacher(admin: CurrentAdmin, lesson_id: int):
    return "Lesson is shown"


@router.post("/lessons", description="Create a new lesson")
async def create_lesson(teacher: CurrentTeacher):
    return "New lesson is added"


@router.patch("/lessons/{lesson_id}", description="Update an existing lesson")
async def edit_lesson(teacher: CurrentTeacher, lesson_id: int):
    return "Current lesson is edited"
