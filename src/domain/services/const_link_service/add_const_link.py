from src.application.dto.const_link import AddConstLinkDTO
from src.infrastructure.repositories import study_group_repository
from src.infrastructure.exceptions import (
    ConstLinkAlreadyExistsException,
    TeacherNotFoundInSubjectException
)

from fastapi import Response, status


async def add(dto: AddConstLinkDTO):
    if not await study_group_repository.has_by_ids(dto.subject_id, dto.teacher_id):
        raise TeacherNotFoundInSubjectException()
    
    study_group_id = await study_group_repository.get_by_ids(dto.teacher_id, dto.subject_id)
    
    if await study_group_repository.has_end_date(study_group_id):
        raise ConstLinkAlreadyExistsException()

    await study_group_repository.update_by_id(
        study_group_id, 
        {"const_end_date": dto.end_date}
    )
    return Response(status_code=status.HTTP_201_CREATED)
