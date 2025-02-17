from src.domain.helpers.schedule import get_last_monday
from src.application.dto.schedule import AddLessonInScheduleDTO
from src.infrastructure.enums.week import Week
from src.infrastructure.repositories import (
    schedule_repository, 
    teacher_repository,
    lesson_repository, 
    study_group_repository,
)
from src.infrastructure.exceptions import (
    TeacherNotFoundException,
    TeacherNotFoundInSubjectException,
    ScheduleLessonNotFoundException,
    InitialFromScheduleException
)

from fastapi import Response, status
from typing import List
from datetime import date
from uuid import UUID


async def add_many(teacher_id: UUID, dto: List[AddLessonInScheduleDTO]):
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    subject_ids = [i.subject_id for i in dto]
    if not await study_group_repository.has_by_subjects(teacher_id, subject_ids):
        raise TeacherNotFoundInSubjectException()
    
    week = get_last_monday()
    if not await schedule_repository.has_by_id(teacher_id):
        await schedule_repository.add(teacher_id, week)
        schedule_id = await schedule_repository.get_by_id(teacher_id)
    else:
        schedule_id = await schedule_repository.get_by_id(teacher_id)
        await schedule_repository.update_by_id(
            schedule_id,
            {"week_start": week}
        )
    
    dto_list = [i.model_dump(exclude_none=True) for i in dto]
    for i in dto_list:
        if i["week"] == "all":
            i["week"] = Week.FIRST
            dto_list.append(i.copy())
            i["week"] = Week.SECOND
    
    await schedule_repository.add_lessons(schedule_id, dto_list)
    return Response(status_code=status.HTTP_201_CREATED)
    

async def add(teacher_id: UUID, dto: AddLessonInScheduleDTO):
    return await add_many(teacher_id, [dto])
    

async def add_scheduled(
    teacher_id: UUID, 
    schedule_lesson_id: UUID, 
    date: date
):
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise ScheduleLessonNotFoundException()
    
    schedule_lesson = await schedule_repository.get_lesson_by_id(schedule_lesson_id)

    if date.weekday() != schedule_lesson.day:
        raise InitialFromScheduleException()

    try: 
        study_group_id = await study_group_repository.get_by_ids(
            teacher_id, 
            schedule_lesson.subject_id
        )
    except Exception:
        raise TeacherNotFoundInSubjectException()

    if await lesson_repository.has_by_schedule(
        study_group_id, schedule_lesson, date
    ):
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
