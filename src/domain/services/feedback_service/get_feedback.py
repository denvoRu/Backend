from src.domain.helpers.feedback import get_excel_file_with_feedbacks
from src.infrastructure.constants.excel import XLSX_MEDIA_TYPE
from src.infrastructure.enums.role import Role
from src.infrastructure.enums.privilege import Privilege
from src.domain.extensions.check_role.user import User
from src.infrastructure.exceptions import (
    LessonNotFoundException,
    FeedbacksNotFoundException,
    NotHaveEnoughPrivilegesException
)
from src.infrastructure.repositories import (
    feedback_repository, 
    lesson_repository,
    teacher_repository
)

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
        raise LessonNotFoundException()

    if user.role == Role.TEACHER and user.id and \
       not await lesson_repository.is_teacher_of_lesson(
        user.id, 
        lesson_id
    ):
        raise LessonNotFoundException()

    if user.role == Role.TEACHER and \
       not await teacher_repository.privilege.has_by_name(
        user.id, 
        Privilege.SEE_COMMENTS
    ):
        raise NotHaveEnoughPrivilegesException()
    

    return await feedback_repository.get_all(    
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
        raise LessonNotFoundException()
    

    if user.role == Role.TEACHER and user.id and \
       not await lesson_repository.is_teacher_of_lesson(
        user.id, 
        lesson_id
    ):
        raise LessonNotFoundException()
    
    if user.role == Role.TEACHER and not await teacher_repository.privilege.has_by_name(
        user.id, 
        Privilege.SEE_COMMENTS
    ):
        raise NotHaveEnoughPrivilegesException()
    
    try:
        feedbacks, extra_fields = await feedback_repository.get_all_for_excel(
            lesson_id
        )
    except Exception:
        raise FeedbacksNotFoundException()

    if len(feedbacks) == 0:
        raise FeedbacksNotFoundException()
    
    stream = get_excel_file_with_feedbacks(feedbacks, extra_fields)
    response = StreamingResponse(stream, media_type=XLSX_MEDIA_TYPE)
    response.headers["Content-Disposition"] = "attachment; filename=feedbacks.xlsx"
    return response
