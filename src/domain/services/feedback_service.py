from src.application.dto.feedback import AddFeedbackDTO
from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import (
    feedback_repository, lesson_repository
)

from fastapi import HTTPException, Response, status
from uuid import UUID 


async def get_by_id(
    user: User,
    lesson_id: UUID,
    page, 
    limit, 
    sort, 
    search, 
    desc
): 
    if not await lesson_repository.has_by_id(lesson_id):
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    check_teacher = lesson_repository.is_teacher_of_lesson(user.id, lesson_id)

    if user.role == Role.TEACHER and user.id and not await check_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    return feedback_repository.get_all(    
        lesson_id,
        page, 
        limit, 
        sort, 
        search, 
        desc
    )


async def get_xlsx_by_id(lesson_id: UUID): 
    if not await lesson_repository.has_by_id(lesson_id):
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    return ""


async def add(lesson_id: UUID, dto: AddFeedbackDTO):
    if not await lesson_repository.has_active_by_id(lesson_id):
        HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    feedback_dto_dict = dto.model_dump(exclude_none=True, exclude=["extra_fields"])
    extra_field_dto_dict = [
        i.model_dump(exclude_none=True) for i in dto.extra_fields
    ]

    feedback_id = await feedback_repository.add(lesson_id, feedback_dto_dict)
    await feedback_repository.add_extra_fields(
        lesson_id, feedback_id, extra_field_dto_dict
    )
    return Response(status_code=status.HTTP_200_OK)    
