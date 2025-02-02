from src.domain.services import lesson_service
from src.application.dto.lesson import (
    AddLessonDTO, 
    AddLessonExtraFieldDTO, 
    EditLessonDTO
)
from src.domain.extensions.check_role import (
    CurrentTeacher, 
    CurrentAdmin, 
    CurrentUser
)

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse
from datetime import date
from pydantic import UUID4


router = APIRouter()


@router.get("/", description="Show all lessons")
async def get_my_lessons(
    teacher: CurrentTeacher, 
    start_date: date,
    end_date: date,
    subject_ids: str = None
):
    return await lesson_service.get_all(
        teacher,
        teacher.id, 
        start_date, 
        end_date, 
        subject_ids
    )
    

@router.get("/{teacher_id}", description="Show teacher lessons (for admins)")
async def get_lessons_of_teacher(
    admin: CurrentAdmin, 
    teacher_id: UUID4,
    start_date: date,
    end_date: date,
    subject_ids: str = None
):
    return await lesson_service.get_all(
        admin,
        teacher_id, 
        start_date, 
        end_date,
        subject_ids
    )


@router.get("/active/{lesson_id}", description="Show lesson data if this lesson is active")
async def get_data_of_active_lesson(lesson_id: UUID4):
    return await lesson_service.get_active(lesson_id)


@router.get("/{lesson_id}/members", description="Show members of lesson")
async def get_members_of_lesson(user: CurrentUser, lesson_id: UUID4):
    return await lesson_service.feedback.get_members(
        user, 
        lesson_id
    )


@router.get("/{lesson_id}/members/xlsx", description="Show members of lesson", response_class=StreamingResponse)
async def get_excel_file_with_members_of_lesson(user: CurrentUser, lesson_id: UUID4):
    return await lesson_service.feedback.get_excel_with_members(
        user, 
        lesson_id
    )


@router.get("/{lesson_id}/statistics", description="Show statistics of lesson")
async def get_statistics_of_lesson(user: CurrentUser, lesson_id: UUID4):
    return await lesson_service.feedback.get_statistics(
        user, 
        lesson_id
    )


@router.post("/", description="Add a new lesson", status_code=201)
async def add_lesson(teacher: CurrentTeacher, dto: AddLessonDTO = Body(...)):
    return await lesson_service.add(teacher.id, dto)


@router.post("/{teacher_id}", description="Add a new lesson (for admins)", status_code=201)
async def add_lesson_to_teacher(
    admin: CurrentAdmin, 
    teacher_id: UUID4,
    dto: AddLessonDTO = Body(...)
):
    return await lesson_service.add(teacher_id, dto)


@router.post("/from_modeus", description="Add a new lessons from modeus on week", status_code=201)
async def add_lessons_from_modeus_on_week(
    teacher: CurrentTeacher
):
    return await lesson_service.add_from_modeus_on_week(teacher.id)


@router.post("/{teacher_id}/from_modeus", description="Add a new lessons from modeus on week", status_code=201)
async def add_lessons_from_modeus_on_week(
    admin: CurrentAdmin, 
    teacher_id: UUID4,
):
    return await lesson_service.add_from_modeus_on_week(teacher_id)


@router.post("/{lesson_id}/extra_field", description="Add a new extra field to lesson (universal)", status_code=201)
async def add_extra_field(
    user: CurrentUser, 
    lesson_id: UUID4,
    dto: AddLessonExtraFieldDTO
):
    return await lesson_service.extra_field.add(
        user,
        lesson_id,
        dto
    )


@router.patch("/{lesson_id}", description="Edit an existing lesson (universal)")
async def edit_lesson(
    user: CurrentUser, 
    lesson_id: UUID4, 
    dto: EditLessonDTO = Body(...)
):    
    return await lesson_service.edit(user, lesson_id, dto)


@router.delete("/{lesson_id}", description="Delete a lesson (universal)")
async def delete_lesson(user: CurrentUser, lesson_id: UUID4):
    return await lesson_service.delete(user, lesson_id)


@router.delete("/{lesson_id}/extra_field/{extra_field_id}", description="Delete a extra field from lesson (universal)")
async def delete_extra_field_from_lesson(
    user: CurrentUser,
    lesson_id: UUID4,
    extra_field_id: UUID4
):
    return await lesson_service.extra_field.delete(
        user, 
        lesson_id, 
        extra_field_id
    )
