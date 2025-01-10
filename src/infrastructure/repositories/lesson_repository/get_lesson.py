from src.infrastructure.database.extensions import LESSON_SAVE_FIELDS
from src.infrastructure.database import (
    Lesson, StudyGroup, ScheduleLesson, Subject, get_by_id, db
)

from sqlalchemy import select
from typing import Tuple
from datetime import date, datetime, time
from uuid import UUID


APPENDED = tuple(["subject_name"])


async def get_all(teacher_id: UUID, start_date: date, end_date: date):
    """
    Gets all lessons of teacher
    :param teacher_id: id
    :param start_date: start date of search
    :param end_date: end date of search
    """
    stmt = select(
        Lesson.id,
        Lesson.speaker_name, 
        Lesson.lesson_name,
        Lesson.start_time,
        Lesson.end_time,
        Lesson.date,
        Subject.name.label("subject_name")
    ).select_from(Lesson).join(
        StudyGroup, 
        StudyGroup.id == Lesson.study_group_id
    ).join(
        Subject,
        StudyGroup.subject_id == Subject.id
    ).where(
        Lesson.date >= start_date,
        Lesson.date <= end_date,
        Lesson.is_disabled == False,
        StudyGroup.is_disabled == False,
        StudyGroup.teacher_id == teacher_id
    )
    executed = await db.execute(stmt)
    lessons = executed.all()

    return list(get_formatted_lesson(i, APPENDED) for i in lessons)


async def get_by_id(lesson_id: UUID) -> Lesson:
    return await get_by_id(Lesson, lesson_id)


async def get_end_time_by_id(lesson_id: UUID) -> Tuple[time, date]:
    stmt = select(Lesson.end_time, Lesson.date).where(Lesson.id == lesson_id)
    return (await db.execute(stmt)).one()


async def get_active_by_id(lesson_id: UUID):
    return await get_active_by_condition(Lesson.id == lesson_id)


async def get_active_by_study_group_id(study_group_id: UUID):
    return await get_active_by_condition(Lesson.study_group_id == study_group_id)


async def get_by_schedule(
        study_group_id: UUID, 
        schedule_lesson: ScheduleLesson, 
        date: date
):
    try:
        stmt = select(Lesson.id).where(
            Lesson.study_group_id == study_group_id,
            Lesson.date == date,
            Lesson.start_time == schedule_lesson.start_time,
            Lesson.end_time == schedule_lesson.end_time,
            Lesson.is_disabled == False
        )

        executed = await db.execute(stmt)

        return executed.one()[0]
    except Exception as e:
        await db.commit_rollback()
        raise Exception(str(e))

def get_formatted_lesson(lesson, appended: tuple = ()):
    return {j[0]: j[1] for j in zip(LESSON_SAVE_FIELDS + appended, lesson)}


async def get_active_by_condition(condition):
    now = datetime.now()
    stmt = select(Lesson).where(
        condition,
        Lesson.date >= now.date(),
        Lesson.start_time <= now.time(),
        Lesson.end_time >= now.time(),
        Lesson.is_disabled == False
    )

    try:
        lesson = (await db.execute(stmt)).one()
        return get_formatted_lesson(lesson)
    except Exception:
        db.commit_rollback()
        raise Exception("Lesson not found")
