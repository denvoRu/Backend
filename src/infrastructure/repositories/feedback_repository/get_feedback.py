from src.infrastructure.database import Feedback, ExtraField, db

from sqlalchemy import select, func, distinct
from uuid import UUID


async def get_all(lesson_id: UUID): ...


async def get_statistics(lesson_id: UUID):
    stmt = select(Feedback.mark ,func.count(Feedback.mark)).select_from(Feedback).where(
        Feedback.lesson_id == lesson_id
    ).group_by(Feedback.mark)

    executed = await db.execute(stmt)

    return { str(i): j for i, j in executed.all() }


async def get_members(lesson_id: UUID):
    stmt = distinct(select(Feedback.student_name).where(
        Feedback.lesson_id == lesson_id,
        Feedback.student_name != ""
    ))

    names = await db.execute(stmt)
    return [i[0] for i in names.all()]
