from src.domain.extensions.get_unique_lessons import get_unique_lessons
from src.infrastructure.enums.role import Role
from src.infrastructure.enums.privilege import Privilege
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import (
    lesson_repository, schedule_repository,
    teacher_repository, 
)

from src.infrastructure.exceptions import (
    LessonNotFoundException, 
    TeacherNotFoundException,
)

from fastapi import HTTPException, status
from datetime import date
from uuid import UUID


async def get_all(
    user: User,
    teacher_id: UUID, 
    start_date: date, 
    end_date: date,
    subject_ids: str = None
):
    """
    Gets all lessons of teacher depending on dates
    :param teacher_id: id of teacher
    :param start_date: start date of search
    :param end_date: end date of search
    """
    if not await teacher_repository.has_by_id(teacher_id):  
        raise TeacherNotFoundException()
    
    if not await schedule_repository.has_by_id(teacher_id):
        return []
    
    if subject_ids is not None and len(subject_ids) != 0:
        subject_ids = subject_ids.split(",")
    
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    if (end_date - start_date).days > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interval must be less than 7 days"
        )
    
    if user.role == Role.TEACHER:
        see_rating = await teacher_repository.privilege.has_by_name(
            teacher_id, 
            Privilege.SEE_RATING
        )
    else: 
        see_rating = True
    
    lessons = await lesson_repository.get_all(
        teacher_id, 
        start_date, 
        end_date, 
        subject_ids,
        see_rating=see_rating
    )

    future_lessons = await schedule_repository.get_in_interval(
        teacher_id, 
        start_date, 
        end_date, 
        subject_ids
    )
    lessons.extend(future_lessons)
    
    return get_unique_lessons(lessons)


async def get_active(lesson_id: UUID):
    try:
        return await lesson_repository.get_active_by_id(lesson_id)
    except Exception:
        raise LessonNotFoundException()
    