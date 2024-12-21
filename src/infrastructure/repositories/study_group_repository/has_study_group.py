from src.infrastructure.database import StudyGroup, has_instance


async def has_by_id(subject_id, teacher_id):
    return await has_instance(
        StudyGroup,
        (StudyGroup.subject_id == subject_id, 
         StudyGroup.teacher_id == teacher_id)
    )  
