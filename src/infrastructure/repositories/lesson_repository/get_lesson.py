from src.infrastructure.database.extensions import LESSON_SAVE_FIELDS
from src.infrastructure.database import Lesson, StudyGroup, get_by_id, db

from sqlalchemy import select
from datetime import date
from uuid import UUID


async def get_by_id(lesson_id: UUID):
    return await get_by_id(Lesson, lesson_id)


async def get_all(teacher_id: UUID, start_date: date, end_date: date):
    stmt = select(*[getattr(Lesson, f) for f in LESSON_SAVE_FIELDS])\
        .select_from(Lesson).join(
            StudyGroup, 
            StudyGroup.id == Lesson.study_group_id
        ).where(
            Lesson.date >= start_date,
            Lesson.date <= end_date,
            StudyGroup.teacher_id == teacher_id
        )
    executed = await db.execute(stmt)

    result = executed.scalars().all()

    return list(
        {j[0]: j[1] for j in zip(LESSON_SAVE_FIELDS, i)} for i in result
    )
