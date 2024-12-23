from src.infrastructure.database import (
    ScheduleLesson, delete_from_instance_by_id
)

from uuid import UUID


async def delete_lesson(schedule_lesson_id: UUID):
    return await delete_from_instance_by_id(
        ScheduleLesson, 
        schedule_lesson_id
    )
