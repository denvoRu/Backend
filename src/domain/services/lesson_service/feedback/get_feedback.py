from src.domain.helpers.lesson import get_excel_file_with_members
from src.infrastructure.constants.excel import XLSX_MEDIA_TYPE
from src.infrastructure.enums.role import Role
from src.infrastructure.enums.privilege import Privilege
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import (
    lesson_repository,
    feedback_repository,
    teacher_repository
)
from src.infrastructure.exceptions import (
    FeedbacksNotFoundException,
    LessonNotFoundException, 
    NotHaveEnoughPrivilegesException
)

from fastapi.responses import StreamingResponse
from uuid import UUID


async def get_statistics(user: User, lesson_id: UUID):
    """
    Get statistics of lesson (feedbacks statistics)
    """
    if not await lesson_repository.has_by_id(lesson_id):
        raise LessonNotFoundException()
      

    if user.role == Role.TEACHER and \
       not await lesson_repository.is_teacher_of_lesson(
        user.id, lesson_id
    ):
        raise LessonNotFoundException()
    
    if user.role == Role.TEACHER:
        if not await teacher_repository.privilege.has_by_name(
            user.id, 
            Privilege.SEE_RATING
        ):
            raise NotHaveEnoughPrivilegesException()

    return await feedback_repository.get_statistics(lesson_id)


async def get_members(user: User, lesson_id: UUID):
    if not await lesson_repository.has_by_id(lesson_id):
        raise LessonNotFoundException()

    if user.role == Role.TEACHER and not await lesson_repository.is_teacher_of_lesson(
        user.id, 
        lesson_id
    ):
        raise LessonNotFoundException()

    return await feedback_repository.get_members(lesson_id)


async def get_excel_with_members(user: User, lesson_id: UUID):
    if not await lesson_repository.has_by_id(lesson_id):
        raise LessonNotFoundException()
    
    if user.role == Role.TEACHER:
        if not await lesson_repository.is_teacher_of_lesson(
            user.id, 
            lesson_id
        ):
            raise LessonNotFoundException()
    
    members = await feedback_repository.get_members(lesson_id)

    if not members or len(members) == 0:
        raise FeedbacksNotFoundException()
    
    members = [i["name"] for i in members]

    stream = get_excel_file_with_members(members)

    response = StreamingResponse(stream, media_type=XLSX_MEDIA_TYPE)
    response.headers["Content-Disposition"] = "attachment; filename=members.xlsx"
    return response
