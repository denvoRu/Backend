from src.infrastructure.database.extensions import LESSON_SAVE_FIELDS
from src.infrastructure.database import (
    Schedule, Subject, ScheduleLesson, get, has_instance, db
)

from sqlalchemy import select, text
from datetime import date, timedelta
from uuid import UUID


async def get_by_week(teacher_id: UUID, week: int, filters = []):
    """
    Gets a schedule by needed week with filters
    """
    schedule_id = await get_by_id(teacher_id)
    columns = [
        "schedule_lesson.day",
        "subject.name",
        *["schedule_lesson." + f for f in LESSON_SAVE_FIELDS if f != 'date']
    ]

    stmt = select(*[text(column) for column in columns]).select_from(
        ScheduleLesson,
    ).where(
        ScheduleLesson.schedule_id == schedule_id,
        ScheduleLesson.week == week,
        *filters
    ).join(Subject, Subject.id == ScheduleLesson.subject_id)

    executed = await db.execute(stmt)
    formatted = lambda i: {
        get_clean_column_name(j[0]): j[1] 
        for j in zip(columns, i)
    }
    
    return list(formatted(i) for i in executed.all())


async def get_in_interval(teacher_id: UUID, start: date, end: date):
    """
    Gets a schedule of teacher in the needed interval with start and end dates
    """
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
        ScheduleLesson.day <= end.weekday()
    ])

    result = [replace_day_on_date(i, start) for i in result]

    return result


async def get_lesson_by_id(schedule_lesson_id: UUID):
    return await get.get_by_id(ScheduleLesson, schedule_lesson_id)


async def get_by_id(teacher_id: UUID):
    return await get.get_by_id(
        Schedule, 
        teacher_id,
        attr_name='id',
        id_name='teacher_id'
    )


def get_clean_column_name(column_name: str):
    return (column_name
        .replace('schedule_lesson.id', 'schedule_lesson_id')
        .replace('schedule_lesson.', '')
        .replace('.', '_')
    )


def replace_day_on_date(data: dict, start_date):
    data["date"] = get_first_date_in_future(data["day"], start_date)
    data.pop("day")

    return data
    

def get_first_date_in_future(weekday: int, start_date):
    delta = weekday - start_date.weekday()
    if delta <= 0:
        delta += 7
    return start_date + timedelta(days=delta)
