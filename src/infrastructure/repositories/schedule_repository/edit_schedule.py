from src.infrastructure.database import ScheduleLesson, update_instance

from uuid import UUID


async def update_lesson_by_id(schedule_lesson_id: UUID, dto: dict):
    return await update_instance(
        ScheduleLesson,
        schedule_lesson_id,
        dto
    )