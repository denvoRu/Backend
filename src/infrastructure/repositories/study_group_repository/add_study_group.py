from src.infrastructure.database import StudyGroup, add_instance

from uuid import UUID


async def add(subject_id: UUID, teacher_id: UUID):
    study_group = StudyGroup(
        subject_id=subject_id,
        teacher_id=teacher_id
    )
    await add_instance(study_group)
