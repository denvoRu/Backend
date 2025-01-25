from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import lesson_repository
from src.application.dto.lesson import EditLessonDTO
from src.infrastructure.exceptions import (
    LessonNotFoundException, 
    TimeLessOriginalException,
    NotTodayDateException
)

from fastapi import Response, status
from datetime import datetime
from uuid import UUID


async def edit(user: User, lesson_id: UUID, dto: EditLessonDTO):
    if not await lesson_repository.has_by_id(lesson_id):
        raise LessonNotFoundException()
    
    if user.role == Role.TEACHER and not await lesson_repository.is_teacher_of_lesson(
        user.id, 
        lesson_id
    ):
        raise LessonNotFoundException()
    
    lesson_end_time, date = await lesson_repository.get_end_time_by_id(lesson_id)

    if not(date == datetime.now().date()):    
        raise NotTodayDateException()
    
    if dto.end_time is not None and lesson_end_time > dto.end_time:
        raise TimeLessOriginalException()
    
    dto_dict = dto.model_dump(exclude_none=True)

    await lesson_repository.update_by_id(lesson_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)
