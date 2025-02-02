from src.infrastructure.database import StudyGroup, has_instance


async def has_by_id(study_group_id):
    return await has_instance(
        StudyGroup,
        StudyGroup.id == study_group_id
    )  


async def has_by_ids(subject_id, teacher_id):
    return await has_instance(
        StudyGroup,
        (StudyGroup.subject_id == subject_id, 
         StudyGroup.teacher_id == teacher_id,
         StudyGroup.is_disabled == False)
    )  


async def has_end_date(study_group_id):
    return await has_instance(
        StudyGroup,
        (StudyGroup.id == study_group_id, 
         StudyGroup.const_end_date != None)
    )


async def has_by_subjects(teacher_id, subject_ids):
    return all(
        [await has_by_ids(subject_id, teacher_id) for subject_id in subject_ids]
    )