from src.infrastructure.enums.week import Week
from src.infrastructure.repositories import (
    schedule_repository, 
    teacher_repository, 
    study_group_repository
)
from src.domain.helpers.schedule import (
    get_last_monday, 
    import_from_modeus_by_id
)
from src.infrastructure.exceptions import (
    TeacherNotFoundException,
    TeacherNotFoundInSubjectException
)

from uuid import UUID


async def get_by_teacher(teacher_id: UUID, week: Week = Week.FIRST): 
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    if not await schedule_repository.has_by_id(teacher_id):
        return []
    
    return await schedule_repository.get_by_week(teacher_id, week)


async def get_from_modeus(
    teacher_id: UUID, 
    subject_id: UUID = None
):
    # Create logic with UNION  
    #
    # if week_count != 1 and week_count != 2:
    #    raise HTTPException(
    #        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    #        detail="Week count must be 1 or 2"
    #    ) 
    
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    if subject_id and not await study_group_repository.has_by_ids(subject_id, teacher_id):
        raise TeacherNotFoundInSubjectException()
    
    if not await schedule_repository.has_by_id(teacher_id):
        last_monday = get_last_monday()
        await schedule_repository.add(teacher_id, last_monday)

    return await import_from_modeus_by_id(
        teacher_id, 
        subject_id=subject_id, 
        with_counter=False
    )
