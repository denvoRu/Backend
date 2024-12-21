from src.application.dto.schedule import (
    AddLessonInScheduleDTO, EditLessonInScheduleDTO
)
from src.domain.services import schedule_service
from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin
from fastapi import APIRouter, Body


router = APIRouter()


@router.get("/", description="Show my schedule")
async def get_schedule(teacher: CurrentTeacher, week: int = 1):
    return await schedule_service.get_schedule(teacher.user_id, week)


@router.get("/{teacher_id}", description="Show teacher schedules (for admins)")
async def get_teacher_schedule(admin: CurrentAdmin, teacher_id: int, week: int = 1):
    return await schedule_service.get_schedule(teacher_id, week)


@router.post('/from_modeus', description="Add lessons to my schedule from Modeus")
async def add_lessons_from_modeus(
    teacher: CurrentTeacher
):
    return await schedule_service.import_from_modeus(teacher.user_id)


@router.post("/", description="Add lesson to my schedule")
async def add_lesson_in_schedule(
    teacher: CurrentTeacher, 
    dto: AddLessonInScheduleDTO = Body(...)
):
    return await schedule_service.add_lesson(teacher.user_id, dto)


@router.post("/{teacher_id}", description="Add lesson to teacher schedule (for admins)")
async def add_lesson_in_teacher_schedule(    
    admin: CurrentAdmin, 
    teacher_id: int,
    dto: AddLessonInScheduleDTO = Body(...)
):
    return await schedule_service.add_lesson(teacher_id, dto)


@router.patch("/{schedule_lesson_id}", description="Edit lesson in my schedule")
async def edit_lesson_in_schedule(
    teacher: CurrentTeacher, 
    schedule_lesson_id: int, 
    dto: EditLessonInScheduleDTO
):
    return await schedule_service.edit_lesson(
        teacher.user_id, 
        schedule_lesson_id, 
        dto
    )


@router.patch("/{teacher_id}/{schedule_lesson_id}", description="Edit lesson in teacher schedule (for admins)")
async def edit_lesson_in_teacher_schedule(
    admin: CurrentAdmin, 
    teacher_id: int, 
    schedule_lesson_id: int, 
    dto: EditLessonInScheduleDTO = Body(...)
):
    return await schedule_service.edit_lesson(
        teacher_id, 
        schedule_lesson_id, 
        dto
    )


@router.delete("/{schedule_lesson_id}", description="Delete lesson from my schedule")
async def delete_lesson_from_schedule(teacher: CurrentTeacher, schedule_lesson_id: int):
    return await schedule_service.delete_lesson(
        teacher.user_id, 
        schedule_lesson_id
    )


@router.delete("/{teacher_id}/{schedule_lesson_id}", description="Delete lesson from teacher schedule (for admins)")
async def delete_lesson_from_teacher_schedule(
    admin: CurrentAdmin, 
    teacher_id: int, 
    schedule_lesson_id: int
):
    return await schedule_service.delete_lesson(
        teacher_id, 
        schedule_lesson_id
    )
