from src.infrastructure.database import (
    Schedule, Subject, ScheduleLesson, get_by_id, db
)

from sqlalchemy import select
from uuid import UUID


async def get_by_week(teacher_id: UUID, week: int):
    schedule_id = await get_by_id(teacher_id)

    stmt = select(
        Subject.name,
        ScheduleLesson.day,
        ScheduleLesson.start_time,
        ScheduleLesson.end_time
    ).where(
        ScheduleLesson.schedule_id == schedule_id,
        ScheduleLesson.week == week).join(Subject)

    executed = await db.execute(stmt)
    return executed.scalars().all()


async def get_by_id(teacher_id: UUID):
    return await get_by_id(
        Schedule, 
        teacher_id,
        attr_name='id',
        id_name='teacher_id'
    )
