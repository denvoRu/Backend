from src.infrastructure.config import config
from src.infrastructure.database.extensions.row_to_dict import row_to_dict
from src.infrastructure.database import (
    Schedule, 
    Subject, 
    ScheduleLesson,
    Teacher,
    get, 
    has_instance, 
    db
)

from sqlalchemy import select, and_, func
from typing import List
from aiomodeus.student_voice import ScheduleOfWeek
from datetime import date, timedelta, datetime
from uuid import UUID


async def get_by_week(teacher_id: UUID, week: int, filters = []):
    """
    Gets a schedule by needed week with filters
    """
    schedule_id = await get_by_id(teacher_id)

    stmt = select(
        ScheduleLesson.day.label("day"),
        ScheduleLesson.subject_id.label("subject_id"),
        Subject.name.label("subject_name"),
        ScheduleLesson.id.label("schedule_lesson_id"),
        ScheduleLesson.speaker_name,
        func.concat(
            Teacher.second_name, 
            " ", 
            Teacher.first_name, 
            " ", 
            Teacher.third_name
        ).label("teacher_name"), 
        ScheduleLesson.week,
        ScheduleLesson.lesson_name,
        ScheduleLesson.start_time,
        ScheduleLesson.end_time,
        ScheduleLesson.end_date
    ).select_from(
        ScheduleLesson,
    ).join(
        Schedule,
        Schedule.id == ScheduleLesson.schedule_id
    ).join(
        Teacher, 
        Teacher.id == Schedule.teacher_id
    ).where(
        ScheduleLesson.schedule_id == schedule_id,
        ScheduleLesson.week == week,
        and_(
            ScheduleLesson.end_date is not None,
            ScheduleLesson.end_date >= date.today()
        ),
        *filters
    ).join(Subject, Subject.id == ScheduleLesson.subject_id)

    executed = await db.execute(stmt)
    
    return list(row_to_dict(i) for i in executed.all())


async def get_in_interval(
    teacher_id: UUID, 
    start: date, 
    end: date,
    subject_ids: List[UUID] = None,
):
    """
    Gets a schedule of teacher in the needed interval with start and end dates
    """
    filters = []
    now_date = datetime.now().date()

    if start > config.END_OF_SEMESTR or end < now_date:
        return []
    
    if start < now_date:
        start = now_date
    
    if subject_ids is not None and len(subject_ids) > 0:
        filters.append(ScheduleLesson.subject_id.in_(subject_ids))

    schedule = await db.execute(
        select(Schedule.id, Schedule.week_start)
        .where(
            Schedule.teacher_id == teacher_id,
            Schedule.is_disabled == False
        )
    )
    schedule = schedule.one()

    has_second_week = await has_instance(ScheduleLesson, (
        ScheduleLesson.week == 1,
        ScheduleLesson.schedule_id == schedule.id
    ))
    week_start = schedule.week_start

    if has_second_week and (((start - week_start).days // 7) % 2 == 1):
        current_week = 1
    else:
        current_week = 0

    result = await get_by_week(teacher_id, current_week, filters=[
        ScheduleLesson.day >= start.weekday(),
        ScheduleLesson.day <= end.weekday(),
        *filters
    ])

    result = [replace_day_on_date(i, start) for i in result]

    return result


async def get_lesson_by_id(schedule_lesson_id: UUID):
    return await get.get_by_id(ScheduleLesson, schedule_lesson_id)


async def get_by_id(teacher_id: UUID):
    return await get.get_by_id(
        Schedule, 
        teacher_id,
        attr_name="id",
        id_name="teacher_id"
    )


async def get_exists_by_subject_id(
    schedule: ScheduleOfWeek, 
    subject_id: UUID = None
) -> List[dict]:
    lessons = []
    for i in schedule.schedule_lessons.get_in_unique_time():
        lesson_subject_id = await i.find_subject_id(db, Subject)
        
        if lesson_subject_id is not None:
            if subject_id is not None and lesson_subject_id != subject_id:
                continue

            lesson = i.model_dump(
                exclude_none=True, 
                exclude={
                    "id", 
                    "subject"
                }
            )

            lesson["subject_id"] = lesson_subject_id
            lessons.append(lesson)

    return lessons


def get_clean_column_name(column_name: str):
    return (column_name
        .replace("schedule_lesson.id", "schedule_lesson_id")
        .replace("schedule_lesson.", "")
        .replace(".", "_")
    )


def replace_day_on_date(data: dict, start_date):
    data["date"] = get_first_date_in_future(data["day"], start_date)
    data.pop("day")

    return data
    

def get_first_date_in_future(weekday: int, start_date):
    delta = weekday - start_date.weekday()
    if delta < 0:
        delta += 6
    return start_date + timedelta(days=delta)
