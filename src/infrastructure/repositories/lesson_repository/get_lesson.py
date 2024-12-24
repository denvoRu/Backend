from src.infrastructure.database.extensions import LESSON_SAVE_FIELDS
from src.infrastructure.database import (
    Lesson, StudyGroup, ScheduleLesson, get_by_id, db
)

from sqlalchemy import select
from datetime import date, datetime
from uuid import UUID


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

    lessons = executed.scalars().all()

    return list(get_formatted_lesson(i) for i in lessons)


async def get_by_id(lesson_id: UUID) -> Lesson:
    return await get_by_id(Lesson, lesson_id)


async def get_end_time_by_id(lesson_id: UUID):
    stmt = select(Lesson.end_time).where(Lesson.id == lesson_id)
    return (await db.execute(stmt)).one()[0]


async def get_active_by_id(lesson_id: UUID):
    now = datetime.now()
    stmt = select(Lesson).where(
        Lesson.id == lesson_id,
        Lesson.date >= now.date(),
        Lesson.start_time <= now.time(),
        Lesson.end_time >= now.time()
    )

    lesson = (await db.execute(stmt)).scalars().one()
    return get_formatted_lesson(lesson)


async def get_by_schedule(
        study_group_id: UUID, 
        schedule_lesson: ScheduleLesson, 
        date: date
):
    stmt = select(Lesson.id).where(
        Lesson.study_group_id == study_group_id,
        Lesson.date == date,
        Lesson.start_time == schedule_lesson.start_time,
        Lesson.end_time == schedule_lesson.end_time
    )

    executed = await db.execute(stmt)

    return executed.one()[0]


def get_formatted_lesson(lesson):
    return {j[0]: j[1] for j in zip(LESSON_SAVE_FIELDS, lesson)}