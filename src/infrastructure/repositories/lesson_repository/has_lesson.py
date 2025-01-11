from src.infrastructure.database import Lesson, ScheduleLesson, has_instance

from uuid import UUID
from datetime import date, datetime

"""
Methods that check lesson existence by some parameters
"""


async def has_by_id(lesson_id: UUID):
    return await has_instance(Lesson, Lesson.id == lesson_id)


async def has_active_by_id(lesson_id: UUID, date: date = None):
    now = date if date else datetime.now() 

    return await has_instance(
        Lesson,
        (
            Lesson.id == lesson_id,
            Lesson.date >= now.date(),
            Lesson.start_time <= now.time(),
            Lesson.end_time >= now.time()
        )
    )


async def has_by_schedule(
        study_group_id: UUID,
        schedule_lesson: ScheduleLesson,
        date: date
):
    return await has_instance(
        Lesson,
        (
            Lesson.study_group_id == study_group_id,
            Lesson.date == date,
            Lesson.start_time == schedule_lesson.start_time,
            Lesson.end_time == schedule_lesson.end_time
        )
    )
