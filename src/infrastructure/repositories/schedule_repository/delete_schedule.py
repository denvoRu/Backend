from src.infrastructure.database import (
    ScheduleLesson, delete_from_instance_by_id, db
)

from uuid import UUID
from sqlalchemy import delete


async def delete_lesson(schedule_lesson_id: UUID):
    return await delete_from_instance_by_id(
        ScheduleLesson, 
        schedule_lesson_id
    )


async def delete_all_lessons(schedule_id: UUID):
    stmt = delete(ScheduleLesson).where(
        ScheduleLesson.schedule_id == schedule_id
    )
    await db.execute(stmt)
    await db.commit_rollback()