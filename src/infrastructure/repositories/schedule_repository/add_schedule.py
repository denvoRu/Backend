from src.infrastructure.enums.week import Week
from src.infrastructure.database import (
    Schedule, ScheduleLesson, Subject, add_instance, db
)

from aiomodeus.student_voice import ScheduleLessonList
from uuid import UUID


async def add(teacher_id: UUID, week_start):
    schedule = Schedule(
        teacher_id=teacher_id,
        week_start=week_start
    )
    await add_instance(schedule)


async def add_lesson(schedule_id: UUID, dto: dict):
    """
    Adds a lesson to schedule
    :param schedule_id: id
    :param dto: data of lesson
    """
    schedule_lesson = ScheduleLesson(
        schedule_id=schedule_id,
        **dto
    )
    await add_instance(schedule_lesson)
    return schedule_lesson.id


async def add_lessons(schedule_id: UUID, dto: list):
    for lesson_dto in dto:
        schedule_lesson = ScheduleLesson(
            schedule_id=schedule_id,
            **lesson_dto
        )
        db.add(schedule_lesson)

    await db.commit_rollback()


async def add_lesson_in_all_weeks(schedule_id: UUID, dto: dict):
    for i in Week:
        schedule_lesson = ScheduleLesson(
            schedule_id=schedule_id,
            week=i.value,
            **dto
        )
        db.add(schedule_lesson)

    await db.commit_rollback()

async def add_lesson_from_modeus(
    schedule_id: UUID, 
    schedule: ScheduleLessonList
):
    """
    Adds a lesson to schedule from modeus
    """
    await schedule.add_in_orm(
        schedule_id, 
        db, 
        ScheduleLesson, 
        Subject,
    )
    await db.commit_rollback()
