from src.infrastructure.enums.week import Week
from src.domain.services import schedule_service
from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin, CurrentUser
from src.application.dto.schedule import (
    AddLessonInScheduleDTO, EditLessonInScheduleDTO
)

from fastapi import APIRouter, Body
from pydantic import UUID4


router = APIRouter()


@router.get("/", description="Show my schedule")
async def get_my_schedule(teacher: CurrentTeacher, week: Week = 0):
    return await schedule_service.get_by_teacher_id(teacher.user_id, week)


@router.get("/{teacher_id}", description="Show teacher schedule (for admins)")
async def get_schedule_of_teacher(admin: CurrentAdmin, teacher_id: UUID4, week: Week = 0):
    return await schedule_service.get_by_teacher_id(teacher_id, week)


@router.post('/import_from_modeus', description="Add lessons to my schedule from Modeus", status_code=201)
async def import_lessons_from_modeus(
    teacher: CurrentTeacher
):
    return await schedule_service.import_from_modeus(teacher.user_id)


@router.post("/", description="Add lesson to my schedule", status_code=201)
async def add_lesson_in_my_schedule(
    teacher: CurrentTeacher, 
    dto: AddLessonInScheduleDTO = Body(...)
):
    return await schedule_service.add_lesson(teacher.user_id, dto)


@router.post("/{teacher_id}", description="Add lesson to teacher schedule (for admins)", status_code=201)
async def add_lesson_in_schedule_of_teacher(    
    admin: CurrentAdmin, 
    teacher_id: UUID4,
    dto: AddLessonInScheduleDTO = Body(...)
):
    return await schedule_service.add_lesson(teacher_id, dto)


@router.patch("/{schedule_lesson_id}", description="Edit lesson in my schedule")
async def edit_lesson_in_schedule(
    user: CurrentUser, 
    schedule_lesson_id: UUID4, 
    dto: EditLessonInScheduleDTO
):
    return await schedule_service.edit_lesson(user, schedule_lesson_id, dto)


@router.delete("/{schedule_lesson_id}", description="Delete lesson from my schedule")
async def delete_lesson_from_schedule(user: CurrentUser, schedule_lesson_id: UUID4):
    return await schedule_service.delete_lesson(user, schedule_lesson_id)
