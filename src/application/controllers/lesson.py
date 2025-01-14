from src.application.dto.lesson import EditLessonDTO
from src.domain.services import lesson_service
from src.domain.extensions.check_role import (
    CurrentTeacher, CurrentAdmin, CurrentUser
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
    return await lesson_service.get_members(user, lesson_id)


@router.get("/{lesson_id}/members/xlsx", description="Show members of lesson", response_class=StreamingResponse)
async def get_excel_file_with_members_of_lesson(user: CurrentUser, lesson_id: UUID4):
    return await lesson_service.get_excel_with_members(user, lesson_id)


@router.patch('/{lesson_id}', description='Edit an existing lesson')
async def edit_lesson(
    user: CurrentUser, 
    lesson_id: UUID4, 
    dto: EditLessonDTO = Body(...)
):
    return await lesson_service.edit_lesson(user, lesson_id, dto)


@router.get("/{lesson_id}/statistics", description="Show statistics of lesson")
async def get_statistics_of_lesson(user: CurrentUser, lesson_id: UUID4):
    return await lesson_service.get_statistics(user, lesson_id)
