from .get_schedule import get_by_id
from src.infrastructure.database import (
    Schedule, ScheduleLesson, has_instance
)

from uuid import UUID
from datetime import datetime


"""
Methods that check schedule existence by some parameters
"""


async def has_by_id(teacher_id: UUID):
    return await has_instance(
        Schedule,
        Schedule.teacher_id == teacher_id
    )


async def has_lesson(schedule_lesson_id: UUID):
    return await has_instance(
        ScheduleLesson,
        ScheduleLesson.id == schedule_lesson_id
    )


async def has_by_now(teacher_id: UUID):
    schedule_id = await get_by_id(teacher_id)
    datetime_now = datetime.now()
    week_day = datetime_now.date().weekday()
    time = datetime_now.time()
    # only for one lesson in one time
    return await has_instance(
        ScheduleLesson,
        (
            ScheduleLesson.id == schedule_id,
            ScheduleLesson.day == week_day,
            ScheduleLesson.start_time >= time,
            ScheduleLesson.end_time <= time
        )
    ) 