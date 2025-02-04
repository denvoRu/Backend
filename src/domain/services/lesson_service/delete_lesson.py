from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import (
    lesson_repository, feedback_repository,
)
from src.infrastructure.exceptions import (
    LessonNotFoundException, 
    DeleteLessonWithFeedbackException,
)

from fastapi import Response, status
from uuid import UUID


async def delete(user: User, lesson_id: UUID):
    if user.role == Role.TEACHER and \
       not await lesson_repository.is_teacher_of_lesson(user.id, lesson_id):
        raise LessonNotFoundException()
    
    if await feedback_repository.has_feedback_by_lesson(lesson_id):
        raise DeleteLessonWithFeedbackException()

    if not await lesson_repository.has_by_id(lesson_id):
        raise LessonNotFoundException()
    
    await lesson_repository.delete_by_id(lesson_id)
    return Response(status_code=status.HTTP_200_OK)
