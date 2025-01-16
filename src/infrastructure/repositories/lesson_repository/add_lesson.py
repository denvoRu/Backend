from src.infrastructure.database import Lesson, ScheduleLesson, add_instance

from uuid import UUID
from datetime import date, datetime


async def add(dto: dict):
    lesson = Lesson(**dto)
    await add_instance(lesson)


async def add_lesson_by_schedule(
    study_group_id: UUID, 
    study_group_end_date: date,
    schedule_lesson: ScheduleLesson, 
    date: date
):
    """
    Adds a lesson from schedule
    :param study_group_id: id of the study group
    :param schedule_lesson: lesson from schedule
    :param date: date of the lesson
    """
    date_now = datetime.now().date()

    if study_group_end_date is None or date_now > study_group_end_date:
        study_group_access = False
    else: 
        study_group_access = True

    lesson = Lesson(
        study_group_id=study_group_id,
        lesson_name=schedule_lesson.lesson_name,
        speaker_name=schedule_lesson.speaker_name,
        date=date,
        start_time=schedule_lesson.start_time,
        end_time=schedule_lesson.end_time,
        study_group_access=study_group_access
    )

    await add_instance(lesson)
    return lesson.id