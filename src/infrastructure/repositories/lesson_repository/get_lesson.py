from src.infrastructure.database import (
    Lesson, get_by_id, db
)

from sqlalchemy import select
from uuid import UUID


async def get_by_id(lesson_id: UUID):
    return await get_by_id(Lesson, lesson_id)


async def get_all(teacher_id: UUID):
    stmt = select().where()
    executed = await db.execute(stmt)

    return executed.scalars().all()
