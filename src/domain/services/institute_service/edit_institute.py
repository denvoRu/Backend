from src.application.dto.institute import EditInstituteDTO
from src.infrastructure.repositories import institute_repository
from src.infrastructure.exceptions import InstituteNotFoundException

from fastapi import Response, status
from uuid import UUID


async def edit(institute_id: UUID, dto: EditInstituteDTO):
    if not await institute_repository.has_by_id(institute_id):
        raise InstituteNotFoundException()
    
    await institute_repository.update_by_id(
        institute_id, 
        dto.model_dump(exclude_none=True)
    )
    return Response(status_code=status.HTTP_200_OK)
