from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin
from fastapi import APIRouter


router = APIRouter()


@router.get("/", description="Show my schedule")
def get_schedule(teacher: CurrentTeacher, week: int = 1):
    return "Schedule is shown"


@router.get("/{teacher_id}", description="Show teacher schedules (for admins)")
def get_teacher_schedule(admin: CurrentAdmin, teacher_id: int, week: int = 1):
    return "Schedules are shown"


@router.post('/from_modeus', description="Add lessons to my schedule from Modeus")
def add_lessons_from_modeus(teacher: CurrentTeacher):
    return "Schedule is updated"


@router.post("/", description="Add lesson to my schedule")
def add_lesson_in_schedule(teacher: CurrentTeacher):
    return "Schedule is updated"


@router.post("/{teacher_id}", description="Add lesson to teacher schedule (for admins)")
def add_lesson_in_teacher_schedule(admin: CurrentAdmin, teacher_id: int):
    return "Schedule is updated"


@router.delete("/{schedule_lesson_id}", description="Delete lesson from my schedule")
def delete_lesson_from_schedule(teacher: CurrentTeacher, schedule_lesson_id: int):
    return "Schedule is updated"


@router.delete("/{teacher_id}/{schedule_lesson_id}", description="Delete lesson from teacher schedule (for admins)")
def delete_lesson_from_teacher_schedule(
    teacher: CurrentTeacher, 
    teacher_id: int, 
    schedule_lesson_id: int
):
    return "Schedule is updated"
