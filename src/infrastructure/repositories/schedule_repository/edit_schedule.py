from src.infrastructure.database import (
    Schedule, ScheduleLesson, update_instance
)

from uuid import UUID


async def update_lesson_by_id(schedule_lesson_id: UUID, dto: dict):
    return await update_instance(
        ScheduleLesson,
        schedule_lesson_id,
        dto
    )


async def update_by_id(schedule_id: UUID, dto: dict):
    return await update_instance(
        Schedule,
        schedule_id,
        dto
    )