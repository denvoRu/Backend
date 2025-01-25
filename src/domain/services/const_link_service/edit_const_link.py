from src.application.dto.const_link import EditConstLinkDTO
from src.infrastructure.exceptions import ConstLinkNotFoundException
from src.infrastructure.repositories import study_group_repository

from fastapi import Response, status
from uuid import UUID


async def edit(const_link_id: UUID, dto: EditConstLinkDTO):
    if not await study_group_repository.has_by_id(const_link_id) or \
       not await study_group_repository.has_end_date(const_link_id):
        raise ConstLinkNotFoundException()
    
    await study_group_repository.update_by_id(
        const_link_id, 
        {"const_end_date": dto.end_date}
    )
    return Response(status_code=status.HTTP_200_OK)
