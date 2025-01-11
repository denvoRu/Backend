from src.infrastructure.enums.week import Week
from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.domain.extensions import selenium
from src.domain.helpers.schedule import get_last_monday
from src.infrastructure.repositories import (
    schedule_repository, teacher_repository,
    lesson_repository, study_group_repository,
    subject_repository, module_repository
)
from src.application.dto.schedule import (
    AddLessonInScheduleDTO, EditLessonInScheduleDTO
)

from fastapi import HTTPException, Response, status
from aiomodeus import AioModeus
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
    
    if not await study_group_repository.has_by_id(teacher_id, dto.subject_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Teacher not found in subject"
        )
    
    if not await schedule_repository.has_by_id(teacher_id):
        week = get_last_monday()
        await schedule_repository.add(teacher_id, week)

    dto_dict = dto.model_dump(exclude_none=True)
    schedule_id = await schedule_repository.get_by_id(teacher_id)

    await schedule_repository.add_lesson(schedule_id, dto_dict)
    return Response(status_code=status.HTTP_201_CREATED)
    

async def delete_lesson(user: User, schedule_lesson_id: UUID):
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    check_teacher = schedule_repository.is_teacher_of_lesson(
        user.id, schedule_lesson_id
    )
    
    if user.role == Role.TEACHER and not await check_teacher:
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
    
    check_teacher = schedule_repository.is_teacher_of_lesson(
        user.id, schedule_lesson_id
    )
    
    if user.role == Role.TEACHER and not await check_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    dto_dict = dto.model_dump(exclude_none=True)
    await schedule_repository.update_lesson_by_id(schedule_lesson_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)


async def import_from_modeus(teacher_id: UUID, week_count: int): 
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if week_count != 1 and week_count != 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Week count must be 1 or 2"
        )
    
    if not await schedule_repository.has_by_id(teacher_id):
        last_monday = get_last_monday()
        await schedule_repository.add(teacher_id, last_monday)

    schedule_id = await schedule_repository.get_by_id(teacher_id)
    teacher = await teacher_repository.get_by_id(teacher_id)
    FIO = " ".join([
        teacher["second_name"], 
        teacher["first_name"], 
        teacher["third_name"]
    ])

    institute_id = teacher["institute_id"]

    token = selenium.auth()
    aim = AioModeus(token)  
 
    if week_count == 1:
        schedule = await aim.get_schedule_for_week_by_teacher_name(FIO)
        schedules = [schedule]
    else: 
        schedules = await aim.get_schedule_for_two_week_by_teacher_name(FIO)

    

    for schedule in schedules:
        not_founded_modules = await module_repository.not_has_from_modeus(
            institute_id, 
            schedule.unique_modules
        )
        not_founded_subjects = await subject_repository.not_has_from_modeus(
            schedule.unique_subjects
        )

        await module_repository.add_from_list(
            institute_id, 
            [x.name for x in not_founded_modules]
        )
        await subject_repository.add_from_modeus(
            institute_id, 
            not_founded_subjects
        )

        await schedule_repository.delete_all_lessons(schedule_id)

        if len(schedule.schedule_lessons) > 0:
            await schedule_repository.add_lesson_from_modeus(
                teacher_id,
                schedule_id, 
                schedule.schedule_lessons.get_in_unique_time()
            )
    
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

    return await lesson_repository.add_lesson_by_schedule(
        study_group_id, 
        schedule_lesson, 
        date
    )
