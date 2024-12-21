from src.infrastructure.database import StudyGroup, add_instance


async def add(subject_id: int, teacher_id: int):
    study_group = StudyGroup(
        subject_id=subject_id,
        teacher_id=teacher_id
    )
    await add_instance(study_group)
