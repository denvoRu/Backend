from src.infrastructure.database import StudyGroup, Lesson, commit_rollback, db

from sqlmodel import select
from uuid import UUID


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
        await commit_rollback()
        raise Exception(str(e))


def get_subject_ids_by_teacher_statement(teacher_ids):
    return (
        select(StudyGroup.subject_id)
        .where(
            StudyGroup.teacher_id.in_(teacher_ids), 
            StudyGroup.is_disabled == False
        )
    )
