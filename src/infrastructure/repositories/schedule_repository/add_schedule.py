from src.infrastructure.database import (
    Schedule, ScheduleLesson, Subject, StudyGroup, add_instance, db
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


async def add_lesson_from_modeus(
    teacher_id: UUID,
    schedule_id: UUID, 
    schedule: ScheduleLessonList
):
    """
    Adds a lesson to schedule from modeus
    """
    await schedule.add_in_orm(
        teacher_id,
        schedule_id, 
        db, 
        ScheduleLesson, 
        Subject,
        StudyGroup
    )
    await db.commit_rollback()
