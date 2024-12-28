from src.infrastructure.database import StudyGroup, commit_rollback, db
from sqlalchemy import delete


async def delete_from_subject(subject_id, teacher_id):
    stmt = delete(StudyGroup).where(
        StudyGroup.subject_id == subject_id,
        StudyGroup.teacher_id == teacher_id
    )

    await db.execute(stmt)
    await commit_rollback()


async def delete_many(teacher_id, subject_ids):
    stmt = delete(StudyGroup).where(
        StudyGroup.teacher_id == teacher_id,
        StudyGroup.subject_id.in_(subject_ids)
    )

    await db.execute(stmt)
    await commit_rollback()
