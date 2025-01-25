from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import lesson_repository
from src.application.dto.lesson import AddLessonExtraFieldDTO
from src.infrastructure.exceptions import (
    LessonNotFoundException, 
    ExtraFieldAlreadyExistsException,
)

from fastapi import Response, status
from uuid import UUID


async def add(
    user: User, 
    lesson_id: UUID, 
    dto: AddLessonExtraFieldDTO
): 
    if user.role == Role.TEACHER:
        if not await lesson_repository.is_teacher_of_lesson(user.id, lesson_id):
            raise LessonNotFoundException()
    else:
        if not await lesson_repository.has_by_id(lesson_id):
            raise LessonNotFoundException()
        
    if await lesson_repository.extra_field.has_by_name(lesson_id, dto.name):
        raise ExtraFieldAlreadyExistsException()
    
    dto_dict = dto.model_dump(exclude_none=True)

    await lesson_repository.extra_field.add(lesson_id, dto_dict)
    return Response(status_code=status.HTTP_201_CREATED)
