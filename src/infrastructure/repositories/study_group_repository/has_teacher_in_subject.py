from src.infrastructure.database import has_instance, StudyGroup


async def has_by_id(subject_id, teacher_id):
    return await has_instance(
        StudyGroup,
        (StudyGroup.subject_id == subject_id, 
         StudyGroup.teacher_id == teacher_id)
    )  