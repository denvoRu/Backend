from src.infrastructure.enums.week import Week
from src.domain.services import schedule_lesson_service
from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin, CurrentUser
from src.application.dto.schedule import (
    AddLessonInScheduleDTO, EditLessonInScheduleDTO
)

from fastapi import APIRouter, Body
from typing import List, Union
from datetime import date
from pydantic import UUID4


router = APIRouter()


@router.get("/", description="Show my schedule")
async def get_my_schedule(teacher: CurrentTeacher, week: Week = 0):
    return await schedule_lesson_service.get_by_teacher(
        teacher.id, 
        week
    )

@router.get("/from_modeus", description="Show lessons from Modeus")
async def get_lessons_from_modeus(
    teacher: CurrentTeacher, 
    subject_id: UUID4 = None,
):
    return await schedule_lesson_service.get_from_modeus(
        teacher.id, 
        subject_id, 
    )

@router.get("/{teacher_id}/from_modeus", description="Show lessons from Modeus (for admins)")
async def get_lessons_of_teacher_from_modeus(
    admin: CurrentAdmin,
    teacher_id: UUID4, 
    subject_id: UUID4 = None,
):
    return await schedule_lesson_service.get_from_modeus(
        teacher_id, 
        subject_id, 
    )

@router.get("/{teacher_id}", description="Show teacher schedule (for admins)")
async def get_schedule_of_teacher(
    admin: CurrentAdmin, 
    teacher_id: UUID4, 
    week: Week = 0
):
    return await schedule_lesson_service.get_by_teacher(
        teacher_id, 
        week
    )


@router.post("/", description="Add lesson to my schedule", status_code=201)
async def add_lesson_in_my_schedule(
    teacher: CurrentTeacher, 
    dto: Union[AddLessonInScheduleDTO, List[AddLessonInScheduleDTO]] = Body(...)
):
    if isinstance(dto, list):
        return await schedule_lesson_service.add_many(teacher.id, dto)
    return await schedule_lesson_service.add(teacher.id, dto)


@router.post("/{teacher_id}", description="Add lesson to teacher schedule (for admins)", status_code=201)
async def add_lesson_in_schedule_of_teacher(    
    admin: CurrentAdmin, 
    teacher_id: UUID4,
    dto: Union[AddLessonInScheduleDTO, List[AddLessonInScheduleDTO]] = Body(...)
):
    if isinstance(dto, list):
        return await schedule_lesson_service.add_many(teacher_id, dto)
    return await schedule_lesson_service.add(teacher_id, dto)


@router.post("/{schedule_lesson_id}/lesson", description="Add a lesson from the schedule to the scheduled ones")
async def get_lesson_id_of_shedule_lesson(
    teacher: CurrentTeacher, 
    schedule_lesson_id: UUID4,
    date: date
) -> UUID4:
    return await schedule_lesson_service.add_scheduled(
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
    return await schedule_lesson_service.add_scheduled(
        teacher_id, 
        schedule_lesson_id, 
        date
    )


@router.patch("/{schedule_lesson_id}", description="Edit lesson in my schedule (universal)")
async def edit_lesson_in_schedule(
    user: CurrentUser, 
    schedule_lesson_id: UUID4, 
    dto: EditLessonInScheduleDTO
):
    return await schedule_lesson_service.edit(user, schedule_lesson_id, dto)


@router.delete("/{schedule_lesson_id}", description="Delete lesson from my schedule (universal)")
async def delete_lesson_from_schedule(user: CurrentUser, schedule_lesson_id: UUID4):
    return await schedule_lesson_service.delete(user, schedule_lesson_id)
