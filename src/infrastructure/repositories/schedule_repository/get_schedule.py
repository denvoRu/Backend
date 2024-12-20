from src.infrastructure.database import (
    db, Schedule, ScheduleLesson, get_by_id
)
from sqlalchemy import select


async def get_by_week(teacher_id: int, week: int):
    schedule_id = await get_schedule(teacher_id)

    stmt = select(ScheduleLesson).where(
        ScheduleLesson.schedule_id == schedule_id,
        ScheduleLesson.week == week)

    executed = await db.execute(stmt)
    return executed.scalars().all()

async def get_schedule(teacher_id: int):
    return await get_by_id(
        Schedule, 
        teacher_id,
        attr_name='id',
        id_name='teacher_id'
    )