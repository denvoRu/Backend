from src.infrastructure.database.extensions.row_to_dict import row_to_dict
from src.infrastructure.repositories import (
    feedback_repository, 
    schedule_repository,
    teacher_repository,
)
from src.infrastructure.database import (
    ExtraFieldSetting, 
    Lesson, 
    StudyGroup, 
    ScheduleLesson, 
    Subject, 
    Teacher,
    has_instance,
    get_by_id, 
    db
)

from sqlalchemy import select, func
from typing import List, Tuple
from datetime import date, datetime, time
from uuid import UUID


APPENDED = ("rating", "subject_name")


async def get_all(
    teacher_id: UUID, 
    start_date: date, 
    end_date: date,
    subject_ids: List[UUID] = None,
    *, 
    see_rating: bool = False
):
    """
    Gets all lessons of teacher
    :param teacher_id: id
    :param start_date: start date of search
    :param end_date: end date of search
    """
    filters = []
    columns = []

    if see_rating:
        columns.append(Lesson.rating)

    if subject_ids is not None and len(subject_ids) > 0:
        filters.append(StudyGroup.subject_id.in_(subject_ids))

    stmt = select(
        Lesson.id,
        Lesson.speaker_name, 
        func.concat(
            Teacher.second_name, 
            " ", 
            Teacher.first_name, 
            " ", 
            Teacher.third_name
        ).label("teacher_name"),
        Lesson.lesson_name,
        Lesson.start_time,
        Lesson.end_time,
        Lesson.date,
        StudyGroup.subject_id.label("subject_id"),
        Subject.name.label("subject_name"),
        *columns
    ).select_from(Lesson).join(
        StudyGroup, 
        StudyGroup.id == Lesson.study_group_id
    ).join(
        Teacher, 
        Teacher.id == StudyGroup.teacher_id
    ).join(
        Subject,
        StudyGroup.subject_id == Subject.id
    ).where(
        Lesson.date >= start_date,
        Lesson.date <= end_date,
        Lesson.is_disabled == False,
        StudyGroup.is_disabled == False,
        StudyGroup.teacher_id == teacher_id,
        *filters
    )
    executed = await db.execute(stmt)
    lessons = executed.all()

    lessons = list(row_to_dict(i) for i in lessons)

    for i in lessons:
        has_feedback = await feedback_repository.has_feedback_by_lesson(i["id"])
        if has_feedback:
            tag_dict = await feedback_repository.get_tags(i["id"])
        else:
            tag_dict = {}
        tag_list = list(tag_dict.keys())[0:6]

        i["tags"] = [i for i in tag_list]
        i["has_feedback"] = has_feedback

    return lessons

async def get_by_id(lesson_id: UUID) -> Lesson:
    return await get_by_id(Lesson, lesson_id)


async def get_datetimes_by_id(lesson_id: UUID) -> Tuple[time, date]:
    stmt = select(Lesson.start_time, Lesson.end_time, Lesson.date).where(Lesson.id == lesson_id)
    return (await db.execute(stmt)).one()
    

async def get_active_by_id(lesson_id: UUID):
    return await get_active_by_condition(Lesson.id == lesson_id)


async def get_active_by_const_link_id(study_group_id: UUID):
    now = datetime.now()
    now_date = now.date()
    now_time = now.time()

    if await has_instance(Lesson, (
        Lesson.date >= now_date,
        Lesson.start_time <= now_time,
        Lesson.end_time >= now_time,
    )):
        filtered_study_groups = select(StudyGroup.id).where(
            StudyGroup.id == study_group_id,
            StudyGroup.const_end_date >= now_date
        )
        return await get_active_by_condition(
            Lesson.study_group_id.in_(filtered_study_groups)
        )
    
    schedule_lessons = await __find_schedule_lessons_by_date(
        study_group_id, 
        now_date
    )
    if len(schedule_lessons) > 0:
        lesson_id = await __find_by_schedule_lesson_dict(
            study_group_id, 
            schedule_lessons[0], 
            now_date
        )
        return await get_active_by_id(lesson_id)
    else:
        raise Exception("Not found")


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
    

async def get_active_by_condition(*condition):
    now = datetime.now()
    lesson_stmt = select(
        Lesson.id,
        Lesson.speaker_name,
        func.concat(
            Teacher.second_name, 
            " ", 
            Teacher.first_name, 
            " ", 
            Teacher.third_name
        ).label("teacher_name"), 
        Lesson.lesson_name,
        Lesson.start_time,
        Lesson.end_time,
        Lesson.date,
        Subject.name.label("subject_name")
    ).select_from(
        Lesson
    ).join(
        StudyGroup, 
        StudyGroup.id == Lesson.study_group_id
    ).join(
        Teacher, 
        Teacher.id == StudyGroup.teacher_id
    ).join(
            Subject, 
            StudyGroup.subject_id == Subject.id
    ).where(
        *condition,
        Lesson.date >= now.date(),
        Lesson.start_time <= now.time(),
        Lesson.end_time >= now.time(),
        Lesson.is_disabled == False
    )

    field_stmt = select(
        ExtraFieldSetting.id,
        ExtraFieldSetting.extra_field_name
    ).select_from(
        ExtraFieldSetting
    ).join(
        Lesson, 
        Lesson.id == ExtraFieldSetting.lesson_id
    ).where(
        *condition,
        Lesson.date >= now.date(),
        Lesson.start_time <= now.time(),
        Lesson.end_time >= now.time(),
        Lesson.is_disabled == False
    )

    try:
        lesson = (await db.execute(lesson_stmt)).one()
        fields = (await db.execute(field_stmt)).all()
        fields = [row_to_dict(field) for field in fields]
        lesson = row_to_dict(lesson)
        lesson["extra_field"] = fields
        
        return lesson
    except Exception as e:
        print("TREUUUUEUEUE", e)
        await db.commit_rollback()
        raise Exception("Lesson not found")


async def __find_schedule_lessons_by_date(
    study_group_id: UUID, 
    date: date
):
    teacher_id = await teacher_repository.get_id_by_study_group(
        study_group_id
    )
    return await schedule_repository.get_in_interval(
        teacher_id, 
        date, 
        date, 
    )


async def __find_by_schedule_lesson_dict(
    study_group_id,
    schedule_lesson: dict,
    date: date
    ):
    schedule_lesson = ScheduleLesson.model_validate(schedule_lesson)
    return await get_by_schedule(
        study_group_id, 
        schedule_lesson, 
        date
    )
