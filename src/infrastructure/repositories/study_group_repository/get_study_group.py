from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.database import (
    StudyGroup, Lesson, Subject, Teacher, Module, db, get_all
)

from sqlalchemy import or_, select, func
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
        StudyGroup.id.label("id"),
        Module.name.label("module_name"),
        Subject.name.label("subject_name"),
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
        instiute_id == Module.institute_id,
        *filters
    )

    count_query = select(func.count(1)).select_from(stmt)
    total_record = (await db.execute(count_query)).scalar() or 0
        
    stmt = stmt.offset((page - 1) * limit).limit(limit)
    total_page = ceil(total_record / limit)

    content = (await db.execute(stmt)).all()

    return PageResponse(
        page_number=page,
        page_size=limit,
        total_pages=total_page,
        total_record=total_record,
        content=content
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


def get_subject_ids_by_teacher_statement(teacher_ids):
    return (
        select(StudyGroup.subject_id)
        .where(
            StudyGroup.teacher_id.in_(teacher_ids), 
            StudyGroup.is_disabled == False
        )
    )
