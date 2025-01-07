from src.domain.helpers.feedback import get_excel_file_with_feedbacks
from src.infrastructure.constants.excel import XLSX_MEDIA_TYPE
from src.application.dto.feedback import AddFeedbackDTO
from src.infrastructure.enums.role import Role
from src.infrastructure.enums.privilege import Privilege
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import (
    feedback_repository, lesson_repository,
    teacher_repository
)

from fastapi import HTTPException, Response, status
from fastapi.responses import StreamingResponse
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
    """
    Gets a feedback by id depending on params if user is allowed to
    """
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

    check_privelege = teacher_repository.privelege.has_by_name(
        user.id, 
        Privilege.SEE_COMMENTS
    )

    if user.role == Role.TEACHER and not await check_privelege:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You don't have enough privileges"
        )
    
    return feedback_repository.get_all(    
        lesson_id,
        page, 
        limit, 
        sort, 
        search, 
        desc
    )


async def get_xlsx_by_id(user: User, lesson_id: UUID):
    """
    Create a xlsx file with feedbacks is user is allowed to
    """
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

    check_privelege = teacher_repository.privelege.has_by_name(
        user.id, 
        Privilege.SEE_COMMENTS
    )

    if user.role == Role.TEACHER and not await check_privelege:
        raise HTTPException(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
            detail="You don't have enough privileges"
        )
    
    feedbacks, extra_fields = await feedback_repository.get_all_for_excel(lesson_id)
    stream = get_excel_file_with_feedbacks(feedbacks, extra_fields)

    response = StreamingResponse(stream, media_type=XLSX_MEDIA_TYPE)
    response.headers["Content-Disposition"] = "attachment; filename=feedbacks.xlsx"
    return response


async def add(lesson_id: UUID, dto: AddFeedbackDTO):
    """
    Add a feedback
    :param lesson_id: id of lesson
    :param dto: feedback data as dto with extra fields if exist
    """
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
