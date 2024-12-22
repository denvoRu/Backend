from src.infrastructure.database import (
    Lesson, get_by_id, db
)
from sqlalchemy import select


async def get_by_id(lesson_id: int):
    return await get_by_id(Lesson, lesson_id)


async def get_all(teacher_id: int):
    stmt = select().where()
    executed = await db.execute(stmt)

    return executed.scalars().all()
