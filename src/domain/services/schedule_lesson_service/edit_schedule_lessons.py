from src.infrastructure.enums.role import Role
from src.application.dto.schedule import EditLessonInScheduleDTO
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import (
    schedule_repository,
    subject_repository
)
from src.infrastructure.exceptions import (
    LessonNotFoundException,
    SubjectNotFoundException,
)

from fastapi import Response, status
from uuid import UUID


async def edit(
    user: User,
    schedule_lesson_id: UUID, 
    dto: EditLessonInScheduleDTO
):  
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise LessonNotFoundException()

    if dto.subject_id and not await subject_repository.has_by_id(dto.subject_id): 
        raise SubjectNotFoundException()
    
    if user.role == Role.TEACHER and \
       not await schedule_repository.is_teacher_of_lesson(
        user.id, schedule_lesson_id
    ):
        raise LessonNotFoundException()

    dto_dict = dto.model_dump(exclude_none=True)
    await schedule_repository.update_lesson_by_id(schedule_lesson_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)
