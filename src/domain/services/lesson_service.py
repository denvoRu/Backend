from src.domain.helpers.lesson import get_excel_file_with_members
from src.infrastructure.constants.excel import XLSX_MEDIA_TYPE
from src.infrastructure.enums.role import Role
from src.infrastructure.enums.privilege import Privilege
from src.application.dto.lesson import EditLessonDTO
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import (
    lesson_repository, schedule_repository,
    study_group_repository, feedback_repository,
    teacher_repository
)

from fastapi import HTTPException, Response, status
from fastapi.responses import StreamingResponse
from datetime import date, datetime
from uuid import UUID


async def get_all(teacher_id: UUID, start_date: date, end_date: date):
    """
    Gets all lessons of teacher depending on dates
    :param teacher_id: id of teacher
    :param start_date: start date of search
    :param end_date: end date of search
    """
    if not await schedule_repository.has_by_id(teacher_id):
        return []
    
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    if (end_date.day - start_date.day) > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interval must be less than 7 days"
        )
    
    lessons = await lesson_repository.get_all(teacher_id, start_date, end_date)

    future_lessons = await schedule_repository.get_in_interval(
        teacher_id,
        start_date, 
        end_date
    )
    lessons.extend(future_lessons)

    return lessons


async def get_active(lesson_id: UUID):
    try:
        return await lesson_repository.get_active_by_id(lesson_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    

async def get_members(user: User, lesson_id: UUID):
    if not await lesson_repository.has_by_id(lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    study_group = await study_group_repository.get_by_lesson(lesson_id)

    if user.role == Role.TEACHER and study_group.teacher_id != user.id:
          raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    return await feedback_repository.get_members(lesson_id)


async def get_excel_with_members(user: User, lesson_id: UUID):
    members = await get_members(user, lesson_id)
    stream = get_excel_file_with_members(members)

    response = StreamingResponse(stream, media_type=XLSX_MEDIA_TYPE)
    response.headers["Content-Disposition"] = "attachment; filename=members.xlsx"
    return response



async def get_statistics(user: User, lesson_id: UUID):
    """
    Get statistics of lesson (feedbacks statistics)
    """
    if not await lesson_repository.has_by_id(lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
      
    check_teacher = await lesson_repository.is_teacher_of_lesson(user.id, lesson_id)

    if user.role == Role.TEACHER and not await check_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    check_privelege = teacher_repository.privelege.has_by_name(
        user.id, 
        Privilege.SEE_RATING
    )

    if user.role == Role.TEACHER and not await check_privelege:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You don't have enough privileges"
        )

    return await feedback_repository.get_statistics(lesson_id)


async def edit_lesson(user: User, lesson_id: UUID, dto: EditLessonDTO):
    if not await lesson_repository.has_by_id(lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    study_group = await study_group_repository.get_by_lesson(lesson_id)

    if user.role == Role.TEACHER and study_group.teacher_id != user.id:
          raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    lesson_end_time, date = await lesson_repository.get_end_time_by_id(lesson_id)

    if date != datetime.now().date():    
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="you cannot change lessons for dates other than today"
        )
    
    if dto.end_time is not None and lesson_end_time <= dto.end_time:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="You cannot set the time less than it was originally"
        )
    
    dto_dict = dto.model_dump(exclude_none=True)

    await lesson_repository.update_by_id(lesson_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)
