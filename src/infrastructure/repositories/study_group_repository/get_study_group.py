from src.infrastructure.database import StudyGroup, Lesson, db, get

from sqlmodel import select
from uuid import UUID


async def get_by_lesson(lesson_id: UUID) -> StudyGroup:
    lessons = select(Lesson.study_group_id).where(Lesson.id == lesson_id)
    study_group = select(StudyGroup).where(StudyGroup.id.in_(lessons))

    return (await db.execute(study_group)).one()


async def get_by_ids(teacher_id : UUID, subject_id: UUID) -> UUID:
    stmt = select(StudyGroup.id).where(
        StudyGroup.teacher_id == teacher_id,
        StudyGroup.subject_id == subject_id
    )

    executed = await db.execute(stmt)

    return executed.one()[0]


def get_subject_ids_by_teacher_statement(teacher_ids):
    return (
        select(StudyGroup.subject_id)
        .where(StudyGroup.teacher_id.in_(teacher_ids))
    )
