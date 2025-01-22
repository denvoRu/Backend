from src.application.dto.const_link import AddConstLinkDTO, EditConstLinkDTO
from src.infrastructure.exceptions import (
    InstituteNotFoundException, 
    ConstLinkNotFoundException,
    ConstLinkAlreadyExistsException,
    TeacherNotFoundInSubjectException
)
from src.infrastructure.repositories import (
    study_group_repository,
    institute_repository,
)

from fastapi import Response, status
from uuid import UUID


async def get_all(
    institute_id: UUID,
    page: int = 1,
    limit: int = 10,
    search: str = None,
):
    if not await institute_repository.has_by_id(institute_id):
        raise InstituteNotFoundException()
    
    return await study_group_repository.get_const_links(
        institute_id,
        page, 
        limit, 
        search, 
    )


async def create(dto: AddConstLinkDTO):
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


async def edit(const_link_id: UUID, dto: EditConstLinkDTO):
    if not await study_group_repository.has_by_id(const_link_id) or \
       not await study_group_repository.has_end_date(const_link_id):
        raise ConstLinkNotFoundException()
    
    
    await study_group_repository.update_by_id(
        const_link_id, 
        {"const_end_date": dto.end_date}
    )
    return Response(status_code=status.HTTP_200_OK)


async def delete(const_link_id: UUID):
    if not await study_group_repository.has_by_id(const_link_id) or \
       not await study_group_repository.has_end_date(const_link_id):
        raise ConstLinkNotFoundException()
    
    
    await study_group_repository.update_by_id(
        const_link_id,
        {"const_end_date": None}
    )
    return Response(status_code=status.HTTP_200_OK)
