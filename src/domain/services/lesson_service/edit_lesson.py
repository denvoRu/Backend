from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import lesson_repository, feedback_repository
from src.application.dto.lesson import EditLessonDTO
from src.infrastructure.exceptions import (
    LessonNotFoundException, 
    UpdateLessonWithFeedbackException,
    FutureDateException
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
    
    if await feedback_repository.has_feedback_by_lesson(lesson_id):
        raise UpdateLessonWithFeedbackException()
    
    start_time, end_time, date = await lesson_repository.get_datetimes_by_id(
        lesson_id
    )

    now = datetime.now()
    if dto.date is not None and dto.date < now.date():    
        raise FutureDateException()
    
    start_time = dto.start_time if dto.start_time is not None else start_time
    end_time = dto.end_time if dto.end_time is not None else end_time
    date = dto.date if dto.date is not None else date

    active = (
        start_time <= now.time() and
        end_time >= now.time() and
        date == now.date()
    )

    if date == now.date() and start_time < now.time() and not active:
        raise FutureDateException()
    
    dto_dict = dto.model_dump(exclude_none=True)

    await lesson_repository.update_by_id(lesson_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)
