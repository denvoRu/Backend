from src.application.dto.feedback import AddFeedbackDTO
from src.infrastructure.exceptions import (
    LessonNotFoundException,
    ExtraFieldNotFoundException,
    FeedbackAlreadyExistsException,
)
from src.infrastructure.repositories import (
    feedback_repository, 
    lesson_repository,
)

from fastapi import Response, status
from uuid import UUID 


async def add(lesson_id: UUID, dto: AddFeedbackDTO):
    """
    Add a feedback
    :param lesson_id: id of lesson
    :param dto: feedback data as dto with extra fields if exist
    """
    if not await lesson_repository.has_active_by_id(lesson_id, dto.created_at):
        raise LessonNotFoundException()
    
    feedback_dto_dict = dto.model_dump(exclude_none=True, exclude={"extra_fields"})

    if await feedback_repository.has_feedback_by_created_at(feedback_dto_dict):
        raise FeedbackAlreadyExistsException()

    feedback_id = await feedback_repository.add(lesson_id, feedback_dto_dict)

    if dto.extra_fields and len(dto.extra_fields) > 0:
        extra_field_dto_dict = [
            i.model_dump(exclude_none=True) for i in dto.extra_fields
        ]
        try: 
            await feedback_repository.add_extra_fields(
                lesson_id, 
                feedback_id, 
                extra_field_dto_dict
            )
        except Exception:
            await feedback_repository.delete_by_id(feedback_id)
            raise ExtraFieldNotFoundException()
    return Response(status_code=status.HTTP_200_OK)    
