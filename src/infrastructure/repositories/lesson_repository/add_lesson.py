from src.infrastructure.repositories import study_group_repository
from src.infrastructure.database import Lesson, ScheduleLesson, add_instance, db

from uuid import UUID
from datetime import date, timedelta, datetime


async def add(dto: dict):
    lesson = Lesson(**dto)
    await add_instance(lesson)


async def add_lesson_by_schedule(
    study_group_id: UUID, 
    schedule_lesson: ScheduleLesson, 
    date: date
):
    """
    Adds a lesson from schedule
    :param study_group_id: id of the study group
    :param schedule_lesson: lesson from schedule
    :param date: date of the lesson
    """
    lesson = Lesson(
        study_group_id=study_group_id,
        lesson_name=schedule_lesson.lesson_name,
        speaker_name=schedule_lesson.speaker_name,
        date=date,
        start_time=schedule_lesson.start_time,
        end_time=schedule_lesson.end_time,
    )

    await add_instance(lesson)
    return lesson.id


async def add_many(lessons: list):
    for lesson in lessons:
        l = Lesson(**lesson)
        db.add(l)

    await db.commit_rollback()


async def add_many_from_modeus(teacher_id: UUID, lessons: list, date: date):
    now = datetime.now()
    date_now = now.date()
    time_now = now.time()

    for lesson in lessons:
        del lesson["week"]
        
        if date_now > (date + timedelta(days=lesson["day"])) and \
            time_now > lesson["start_time"]:
            lesson["date"] = date + timedelta(days=lesson["day"]+1+7)
        else:
            lesson["date"] = date + timedelta(days=lesson["day"]+1)

        try:
            lesson["study_group_id"] = await study_group_repository.get_by_ids(
                teacher_id,
                lesson["subject_id"]
            )
        except Exception: 
            continue
        del lesson["day"]
        del lesson["subject_id"]
        l = Lesson(**lesson)
        db.add(l)

    await db.commit_rollback()
