from src.infrastructure.database import (
    Schedule, ScheduleLesson, has_instance
)

from uuid import UUID

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
