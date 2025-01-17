from src.infrastructure.database import StudyGroup, add_instance

from uuid import UUID
from typing import List


async def add(subject_id: UUID, teacher_id: UUID):
    study_group = StudyGroup(
        subject_id=subject_id,
        teacher_id=teacher_id,
        const_end_date=None
    )
    await add_instance(study_group)


async def add_many(teacher_id: UUID, subject_ids: List[UUID]):
    study_groups = [
        StudyGroup(
            subject_id=subject_id,
            teacher_id=teacher_id,
            const_end_date=None
        )
        for subject_id in subject_ids
    ]

    await add_instance(*study_groups)


async def add_many_teachers(subject_id: UUID, teacher_ids: List[UUID]):
    """
    Creates study groups for one subject and some teachers
    """
    study_groups = [
        StudyGroup(
            subject_id=subject_id,
            teacher_id=teacher_id
        )
        for teacher_id in teacher_ids
    ]

    await add_instance(*study_groups)