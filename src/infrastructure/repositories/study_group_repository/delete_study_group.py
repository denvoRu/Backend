from src.infrastructure.database import StudyGroup, db
from sqlalchemy import update


async def delete_by_subject(subject_id, teacher_id):
    stmt = update(StudyGroup).where(
        StudyGroup.subject_id == subject_id,
        StudyGroup.teacher_id == teacher_id,
        StudyGroup.is_disabled == False
    ).values(is_disabled=True)

    await db.execute(stmt)
    await db.commit_rollback()


async def delete_many(teacher_id, subject_ids):
    stmt = update(StudyGroup).where(
        StudyGroup.teacher_id == teacher_id,
        StudyGroup.subject_id.in_(subject_ids),
        StudyGroup.is_disabled == False
    ).values(is_disabled=True)

    await db.execute(stmt)
    await db.commit_rollback()
