from src.infrastructure.enums.week import Week
from src.domain.services import schedule_service
from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin, CurrentUser
from src.application.dto.schedule import (
    AddLessonInScheduleDTO, EditLessonInScheduleDTO
)

from fastapi import APIRouter, Body
from datetime import date
from pydantic import UUID4


router = APIRouter()


@router.get("/", description="Show my schedule")
async def get_my_schedule(teacher: CurrentTeacher, week: Week = 0):
    return await schedule_service.get_by_teacher_id(teacher.id, week)


@router.get("/{teacher_id}", description="Show teacher schedule (for admins)")
async def get_schedule_of_teacher(
    admin: CurrentAdmin, 
    teacher_id: UUID4, 
    week: Week = 0
):
    return await schedule_service.get_by_teacher_id(teacher_id, week)


@router.post('/import_from_modeus', description="Add lessons to my schedule from Modeus", status_code=201)
async def import_lessons_from_modeus(
    teacher: CurrentTeacher, 
    subject_id: UUID4,
    week_count: int = 1
):
    return await schedule_service.import_from_modeus(
        teacher.id, 
        subject_id, 
        week_count
    )


@router.post("/", description="Add lesson to my schedule", status_code=201)
async def add_lesson_in_my_schedule(
    teacher: CurrentTeacher, 
    dto: AddLessonInScheduleDTO = Body(...)
):
    return await schedule_service.add_lesson(teacher.id, dto)


@router.post("/{schedule_lesson_id}/lesson", description="Add a lesson from the schedule to the scheduled ones")
async def get_lesson_id_of_shedule_lesson(
    teacher: CurrentTeacher, 
    schedule_lesson_id: UUID4,
    date: date
) -> UUID4:
    return await schedule_service.add_lesson_scheduled(
        teacher.id, 
        schedule_lesson_id, 
        date
    )

@router.post("/{teacher_id}/{schedule_lesson_id}/lesson", description="Add a lesson from the teacher schedule to the scheduled ones (for admins)")
async def get_lesson_id_of_teacher_shedule_lesson(
    admin: CurrentAdmin,
    teacher_id: UUID4,
    schedule_lesson_id: UUID4,
    date: date
) -> UUID4:
    return await schedule_service.add_lesson_scheduled(
        teacher_id, 
        schedule_lesson_id, 
        date
    )


@router.post("/{teacher_id}", description="Add lesson to teacher schedule (for admins)", status_code=201)
async def add_lesson_in_schedule_of_teacher(    
    admin: CurrentAdmin, 
    teacher_id: UUID4,
    dto: AddLessonInScheduleDTO = Body(...)
):
    return await schedule_service.add_lesson(teacher_id, dto)


@router.patch("/{schedule_lesson_id}", description="Edit lesson in my schedule (universal)")
async def edit_lesson_in_schedule(
    user: CurrentUser, 
    schedule_lesson_id: UUID4, 
    dto: EditLessonInScheduleDTO
):
    return await schedule_service.edit_lesson(user, schedule_lesson_id, dto)


@router.delete("/{schedule_lesson_id}", description="Delete lesson from my schedule (universal)")
async def delete_lesson_from_schedule(user: CurrentUser, schedule_lesson_id: UUID4):
    return await schedule_service.delete_lesson(user, schedule_lesson_id)
