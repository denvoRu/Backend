from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import lesson_repository
from src.infrastructure.exceptions import (
    LessonNotFoundException, 
    ExtraFieldNotFoundException
)

from fastapi import Response, status
from uuid import UUID


async def delete(
    user: User,
    lesson_id: UUID,
    extra_field_id: UUID
): 
    if user.role == Role.TEACHER:
        if not await lesson_repository.is_teacher_of_lesson(user.id, lesson_id):
            raise LessonNotFoundException()
    else:
        if not await lesson_repository.has_by_id(lesson_id):
            raise LessonNotFoundException()
        
    if not await lesson_repository.extra_field.has_by_id(extra_field_id):
        raise ExtraFieldNotFoundException()
    
    await lesson_repository.extra_field.delete_by_id(extra_field_id)
    return Response(status_code=status.HTTP_200_OK)
