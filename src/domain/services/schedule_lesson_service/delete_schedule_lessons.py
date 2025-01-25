from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import schedule_repository
from src.infrastructure.exceptions import LessonNotFoundException

from fastapi import Response, status
from uuid import UUID


async def delete(user: User, schedule_lesson_id: UUID):
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise LessonNotFoundException()

    if user.role == Role.TEACHER and \
       not await schedule_repository.is_teacher_of_lesson(
        user.id, schedule_lesson_id
    ):
        raise LessonNotFoundException()
    
    await schedule_repository.delete_lesson(schedule_lesson_id)
    return Response(status_code=status.HTTP_200_OK)
