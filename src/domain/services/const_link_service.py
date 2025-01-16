from src.application.dto.const_link import AddConstLinkDTO, EditConstLinkDTO
from src.infrastructure.repositories import (
    study_group_repository,
    institute_repository,
)

from fastapi import Response, HTTPException, status
from uuid import UUID


async def get_all(
    institute_id: UUID,
    page: int = 1,
    limit: int = 10,
    search: str = None,
):
    if not await institute_repository.has_by_id(institute_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Institute not found"
        )
    
    return await study_group_repository.get_const_links(
        institute_id,
        page, 
        limit, 
        search, 
    )


async def create(dto: AddConstLinkDTO):
    if not await study_group_repository.has_by_ids(dto.subject_id, dto.teacher_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Teacher not found in subject"
        )
    
    study_group_id = await study_group_repository.get_by_ids(dto.teacher_id, dto.subject_id)
    
    if await study_group_repository.has_end_date(study_group_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Const link already exists"
        )

    await study_group_repository.update_by_id(
        study_group_id, 
        {"const_end_date": dto.end_date}
    )
    return Response(status_code=status.HTTP_201_CREATED)


async def edit(const_link_id: UUID, dto: EditConstLinkDTO):
    if not await study_group_repository.has_by_id(const_link_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Const link not found"
        )
    
    if not await study_group_repository.has_end_date(const_link_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Const link not found"
        )
    
    await study_group_repository.update_by_id(
        const_link_id, 
        {"const_end_date": dto.end_date}
    )
    return Response(status_code=status.HTTP_200_OK)


async def delete(const_link_id: UUID):
    if not await study_group_repository.has_by_ids(const_link_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Const link not found"
        )
    
    if not await study_group_repository.has_end_date(const_link_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Const link not found"
        )
    
    await study_group_repository.update_by_id(
        const_link_id,
        {"const_end_date": None}
    )
    return Response(status_code=status.HTTP_200_OK)
