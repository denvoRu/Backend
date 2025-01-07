from src.infrastructure.database import StudyGroup

from sqlalchemy import select
from uuid import UUID


def stmt_get_by_id(teacher_id: UUID, subject_id: UUID):
    """
    Gets study group by teacher and subject ids
    """
    return select(StudyGroup.teacher_id).where(
        StudyGroup.subject_id == subject_id,
        StudyGroup.teacher_id == teacher_id,
        StudyGroup.is_disabled == False
    )