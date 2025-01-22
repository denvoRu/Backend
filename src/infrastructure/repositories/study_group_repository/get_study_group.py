from src.infrastructure.database.extensions.row_to_dict import row_to_dict
from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.models.const_link_with_lessons import (
    ConstLinkWithLessonsResponse
)
from src.infrastructure.database import (
    StudyGroup, 
    Schedule,
    ScheduleLesson, 
    Lesson, 
    Subject, 
    Teacher, 
    Module, 
    db
)


from sqlalchemy import or_, select, func, distinct
from math import ceil
from uuid import UUID


async def get_const_links(
    instiute_id: UUID,
    page: int = 1,
    limit: int = 10,
    search: str = None,
):
    filters = []

    if search is not None:
        name_split = search.lower().split()
        teacher_name = or_(
            *[func.lower(j).like(f"%{i}%") for i in name_split
            for j in (
                Teacher.first_name, 
                Teacher.second_name, 
                Teacher.third_name
            )]
        )
        module_name = or_(
            *[func.lower(Module.name).like(f"%{i}%") for i in name_split]
        )
        subject_name = or_(
            *[func.lower(Subject.name).like(f"%{i}%") for i in name_split]
        )

        filters.append(or_(teacher_name, module_name, subject_name))

    stmt = select(
        distinct(StudyGroup.id).label("id"),
        Module.id.label("module_id"),
        Module.name.label("module_name"),
        Subject.id.label("subject_id"),
        Subject.name.label("subject_name"),
        StudyGroup.teacher_id.label("teacher_id"),
        func.concat(
            Teacher.second_name, " ", 
            Teacher.first_name, " ", 
            Teacher.third_name
        ).label("teacher_name"),
        StudyGroup.const_end_date.label("end_date")
    ).join(
        Subject,
        StudyGroup.subject_id == Subject.id
    ).join(
        Module,
        Module.id == Subject.module_id
    ).join(
        Teacher,
        Teacher.id == StudyGroup.teacher_id
    ).where(
        Module.institute_id == instiute_id,
        StudyGroup.const_end_date != None,
        *filters
    )

    count_query = select(func.count(1)).select_from(stmt)
    total_record = (await db.execute(count_query)).scalar() or 0
        
    stmt = stmt.offset((page - 1) * limit).limit(limit)
    total_page = ceil(total_record / limit)

    const_links = (await db.execute(stmt)).all()
    const_links = [row_to_dict(i) for i in const_links]

    teacher_ids = [i["teacher_id"] for i in const_links]

    subject_ids = [i["subject_id"] for i in const_links]
    schedule_lessons = select(Schedule.id).where(
        Schedule.teacher_id.in_(teacher_ids),
        Schedule.is_disabled == False)

    stmt_lessons = select(
        Schedule.teacher_id,
        ScheduleLesson.subject_id,
        ScheduleLesson.week,
        ScheduleLesson.day,
        ScheduleLesson.start_time,
        ScheduleLesson.end_time
    ).join(
        Schedule,
        ScheduleLesson.schedule_id == Schedule.id,
    ).where(
        ScheduleLesson.subject_id.in_(subject_ids),
        ScheduleLesson.schedule_id.in_(schedule_lessons)
    )

    lessons = (await db.execute(stmt_lessons)).all()
    lessons = [row_to_dict(i) for i in lessons]

    content = ConstLinkWithLessonsResponse(
        const_links,
        lessons
    )

    return PageResponse(
        page_number=page,
        page_size=limit,
        total_pages=total_page,
        total_record=total_record,
        content=content.to_list()
    )


async def get_by_lesson(lesson_id: UUID) -> StudyGroup:
    lessons = select(Lesson.study_group_id).where(
        Lesson.id == lesson_id, 
        Lesson.is_disabled == False
    )
    study_group = select(StudyGroup).where(
        StudyGroup.id.in_(lessons),
        StudyGroup.is_disabled == False
    )

    return (await db.execute(study_group)).one()


async def get_by_ids(teacher_id : UUID, subject_id: UUID) -> UUID:
    try:
        stmt = select(StudyGroup.id).where(
            StudyGroup.teacher_id == teacher_id,
            StudyGroup.subject_id == subject_id,
            StudyGroup.is_disabled == False
        )

        executed = await db.execute(stmt)

        return executed.one()[0]
    except Exception as e:
        await db.commit_rollback()
        raise Exception(str(e))
    

async def get_end_time(study_group_id: UUID) -> UUID:
    try:
        stmt = select(StudyGroup.const_end_date).where(
            StudyGroup.id == study_group_id,
            StudyGroup.is_disabled == False
        )

        executed = await db.execute(stmt)

        return executed.one()[0]
    except Exception as e:
        await db.commit_rollback()
        raise Exception(str(e))


def get_subject_ids_by_teacher_statement(
    teacher_ids, 
    not_has_const_link = False
):
    filters = []
    
    if not_has_const_link:
        filters.append(StudyGroup.const_end_date == None)
        

    return (
        select(StudyGroup.subject_id)
        .where(
            StudyGroup.teacher_id.in_(teacher_ids), 
            StudyGroup.is_disabled == False,
            *filters
        )
    )
