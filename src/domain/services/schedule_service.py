from src.infrastructure.enums.week import Week
from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.infrastructure.repositories import (
    schedule_repository, teacher_repository,
    lesson_repository, study_group_repository,
    subject_repository
)
from src.domain.helpers.schedule import (
    get_last_monday, 
    import_from_modeus_by_id
)
from src.application.dto.schedule import (
    AddLessonInScheduleDTO, 
    EditLessonInScheduleDTO
)

from fastapi import HTTPException, Response, status
from datetime import date
from uuid import UUID


async def get_by_teacher_id(teacher_id: UUID, week: Week = Week.FIRST): 
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_by_id(teacher_id):
        return []
    
    return await schedule_repository.get_by_week(teacher_id, week)


async def add_lesson(teacher_id: UUID, dto: AddLessonInScheduleDTO):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await study_group_repository.has_by_ids(dto.subject_id, teacher_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Teacher not found in subject"
        )
    
    if not await schedule_repository.has_by_id(teacher_id):
        week = get_last_monday()
        await schedule_repository.add(teacher_id, week)

    schedule_id = await schedule_repository.get_by_id(teacher_id)
    if dto.week == 'all':
        dto_dict = dto.model_dump(exclude_none=True, exclude={'week'})
        await schedule_repository.add_lesson_in_all_week(
            schedule_id, 
            dto_dict, 
        )
    else:
        dto_dict = dto.model_dump(exclude_none=True)
        await schedule_repository.add_lesson(schedule_id, dto_dict)

    return Response(status_code=status.HTTP_201_CREATED)
    

async def delete_lesson(user: User, schedule_lesson_id: UUID):
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    

    if user.role == Role.TEACHER and \
       not await schedule_repository.is_teacher_of_lesson(
        user.id, schedule_lesson_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    await schedule_repository.delete_lesson(schedule_lesson_id)
    return Response(status_code=status.HTTP_200_OK)


async def edit_lesson(
    user: User,
    schedule_lesson_id: UUID, 
    dto: EditLessonInScheduleDTO
):  
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    if not await subject_repository.has_by_id(dto.subject_id): 
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    
    if user.role == Role.TEACHER and \
       not await schedule_repository.is_teacher_of_lesson(
        user.id, schedule_lesson_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    dto_dict = dto.model_dump(exclude_none=True)
    await schedule_repository.update_lesson_by_id(schedule_lesson_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)


async def import_from_modeus(
    teacher_id: UUID, 
    subject_id: UUID,
    week_count: int
):
    if week_count != 1 and week_count != 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Week count must be 1 or 2"
        ) 
    
    if not(await teacher_repository.has_by_id(teacher_id)):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not(await study_group_repository.has_by_ids(subject_id, teacher_id)):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Teacher not found in subject"
        )
    
    if not(await schedule_repository.has_by_id(teacher_id)):
        last_monday = get_last_monday()
        await schedule_repository.add(teacher_id, last_monday)

    await import_from_modeus_by_id(teacher_id, subject_id, week_count)
    return Response(status_code=status.HTTP_200_OK)


async def add_lesson_scheduled(
    teacher_id: UUID, 
    schedule_lesson_id: UUID, 
    date: date
):
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule lesson not found"
        )
    
    schedule_lesson = await schedule_repository.get_lesson_by_id(schedule_lesson_id)

    if date.weekday() != schedule_lesson.day:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You cannot create a lesson for this day"
        )

    try: 
        study_group_id = await study_group_repository.get_by_ids(
            teacher_id, 
            schedule_lesson.subject_id
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="You cannot create a lesson for this subject"
        )

    has_lesson = lesson_repository.has_by_schedule(
        study_group_id, schedule_lesson, date
    )
    if await has_lesson:
        return await lesson_repository.get_by_schedule(
            study_group_id, 
            schedule_lesson,
            date
        ) 
    
    study_group_end_time = await study_group_repository.get_end_time(
        study_group_id
    )

    return await lesson_repository.add_lesson_by_schedule(
        study_group_id, 
        study_group_end_time,
        schedule_lesson, 
        date
    )
