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

from fastapi import HTTPException, Response, status
from fastapi.responses import StreamingResponse
from datetime import date, datetime
from uuid import UUID


async def get_all(
        user: User,
        teacher_id: UUID, 
        start_date: date, 
        end_date: date,
        subject_ids: str = None
    ):
    """
    Gets all lessons of teacher depending on dates
    :param teacher_id: id of teacher
    :param start_date: start date of search
    :param end_date: end date of search
    """
    if not await teacher_repository.has_by_id(teacher_id):  
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_by_id(teacher_id):
        return []
    
    if subject_ids is not None and len(subject_ids) != 0:
        subject_ids = subject_ids.split(",")
    
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    if (end_date - start_date).days > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interval must be less than 7 days"
        )
    
    if user.role == Role.TEACHER:
        see_rating = await teacher_repository.privilege.has_by_name(
            teacher_id, 
            Privilege.SEE_RATING
        )
    else: 
        see_rating = True
    
    lessons = await lesson_repository.get_all(
        teacher_id, 
        start_date, 
        end_date, 
        subject_ids,
        see_rating=see_rating
    )
    future_lessons = await schedule_repository.get_in_interval(
        teacher_id, 
        start_date, 
        end_date, 
        subject_ids
    )
    lessons.extend(future_lessons)
    
    return get_unique_lessons(lessons)


async def get_active(lesson_id: UUID):
    try:
        return await lesson_repository.get_active_by_id(lesson_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )


async def get_statistics(user: User, lesson_id: UUID):
    """
    Get statistics of lesson (feedbacks statistics)
    """
    if not await lesson_repository.has_by_id(lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
      

    if user.role == Role.TEACHER and \
       not await lesson_repository.is_teacher_of_lesson(
        user.id, lesson_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    if user.role == Role.TEACHER:
        if not await teacher_repository.privilege.has_by_name(
            user.id, 
            Privilege.SEE_RATING
        ):
            raise HTTPException(
                status_code=status.HTTP_405_METHOD_NOT_ALLOWED,
                detail="You don't have enough privileges"
            )

    return await feedback_repository.get_statistics(lesson_id)


async def get_members(user: User, lesson_id: UUID):
    if not await lesson_repository.has_by_id(lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    if user.role == Role.TEACHER and not await lesson_repository.is_teacher_of_lesson(
        user.id, 
        lesson_id
    ):
          raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    return await feedback_repository.get_members(lesson_id)


async def get_excel_with_members(user: User, lesson_id: UUID):
    if not await lesson_repository.has_by_id(lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    if user.role == Role.TEACHER:
        if not await lesson_repository.is_teacher_of_lesson(
            user.id, 
            lesson_id
        ):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
    
    members = await feedback_repository.get_members(lesson_id)

    if not members or len(members) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Members not found"
        )
    
    members = [i["name"] for i in members]

    stream = get_excel_file_with_members(members)

    response = StreamingResponse(stream, media_type=XLSX_MEDIA_TYPE)
    response.headers["Content-Disposition"] = "attachment; filename=members.xlsx"
    return response


async def add(teacher_id: UUID, dto: AddLessonDTO):
    now = datetime.now()

    if dto.date < now.date():
        if dto.start_time < now.time():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Start time and date must be in the future"
            )
        
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Date must be in the future"
        )
    
    if dto.start_time > dto.end_time:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Start time must be before end time"
        )

    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await subject_repository.has_by_id(dto.subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

    if not await study_group_repository.has_by_ids(dto.subject_id, teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found in subject"
        )
    
    if not await schedule_repository.has_by_id(teacher_id):
        await schedule_repository.add(teacher_id, get_last_monday())
    
    study_group_id = await study_group_repository.get_by_ids(
        teacher_id, 
        dto.subject_id
    )

    dto = dto.model_dump(
        exclude_none=True, 
        exclude={"subject_id"}, 
    )
    dto['study_group_id'] = study_group_id
    return await lesson_repository.add(dto)
    

async def edit_lesson(user: User, lesson_id: UUID, dto: EditLessonDTO):
    if not await lesson_repository.has_by_id(lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    if user.role == Role.TEACHER and not await lesson_repository.is_teacher_of_lesson(
        user.id, 
        lesson_id
    ):
          raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    lesson_end_time, date = await lesson_repository.get_end_time_by_id(lesson_id)

    if not(date == datetime.now().date()):    
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="you cannot change lessons for dates other than today"
        )

    if dto.end_time is not None and lesson_end_time > dto.end_time:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="You cannot set the time less than it was originally"
        )
    
    dto_dict = dto.model_dump(exclude_none=True)

    await lesson_repository.update_by_id(lesson_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)


async def delete(user: User, lesson_id: UUID):
    if user.role == Role.TEACHER and \
       not await lesson_repository.is_teacher_of_lesson(user.id, lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    if await feedback_repository.has_feedback_by_lesson(lesson_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="You cannot delete a lesson with feedback"
        )

    if not await lesson_repository.has_by_id(lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    await lesson_repository.delete_by_id(lesson_id)
    return Response(status_code=status.HTTP_200_OK)


async def add_extra_field(
    user: User, 
    lesson_id: UUID, 
    dto: AddLessonExtraFieldDTO
): 
    if user.role == Role.TEACHER:
        if not await lesson_repository.is_teacher_of_lesson(user.id, lesson_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
    else:
        if not await lesson_repository.has_by_id(lesson_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
        
    if await lesson_repository.extra_field.has_by_name(lesson_id, dto.name):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Extra field already exists"
        )
    
    dto_dict = dto.model_dump(exclude_none=True)

    await lesson_repository.extra_field.add(lesson_id, dto_dict)
    return Response(status_code=status.HTTP_201_CREATED)


async def delete_extra_field(
    user: User,
    lesson_id: UUID,
    extra_field_id: UUID
): 
    if user.role == Role.TEACHER:
        if not await lesson_repository.is_teacher_of_lesson(user.id, lesson_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
    else:
        if not await lesson_repository.has_by_id(lesson_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lesson not found"
            )
        
    if not await lesson_repository.extra_field.has_by_id(extra_field_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="extra field not found"
        )
    
    await lesson_repository.extra_field.delete_by_id(extra_field_id)
    return Response(status_code=status.HTTP_200_OK)
