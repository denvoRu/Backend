from src.domain.helpers.schedule.last_monday import get_last_monday
from src.domain.helpers.lesson import get_excel_file_with_members
from src.infrastructure.constants.excel import XLSX_MEDIA_TYPE
from src.domain.extensions.get_unique_lessons import get_unique_lessons
from src.infrastructure.enums.role import Role
from src.infrastructure.enums.privilege import Privilege
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import (
    lesson_repository, schedule_repository,
    study_group_repository, feedback_repository,
    teacher_repository, subject_repository
)
from src.application.dto.lesson import (
    EditLessonDTO, 
    AddLessonDTO, 
    AddLessonExtraFieldDTO
)
from src.infrastructure.exceptions import (
    SubjectNotFoundException,
    FeedbacksNotFoundException,
    LessonNotFoundException, 
    TeacherNotFoundException,
    ExtraFieldNotFoundException,
    ExtraFieldAlreadyExistsException,
    NotHaveEnoughPrivilegesException,
    TimeLessOriginalException,
    DeleteLessonWithFeedbackException,
    NotTodayDateException
)

from fastapi import HTTPException, Response, status
from fastapi.responses import StreamingResponse
from datetime import date, datetime
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