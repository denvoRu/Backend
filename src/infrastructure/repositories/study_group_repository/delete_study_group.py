from src.infrastructure.database import StudyGroup, db, commit_rollback
from sqlalchemy import delete


async def delete_from_subject(subject_id, teacher_id):
    stmt = delete(StudyGroup).where(
        StudyGroup.subject_id == subject_id,
        StudyGroup.teacher_id == teacher_id
    )

    await db.execute(stmt)
    await commit_rollback()