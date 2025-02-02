from src.application.dto.institute import AddInstituteDTO
from src.infrastructure.repositories import institute_repository
from src.infrastructure.exceptions import InstituteAlreadyExistsException

from fastapi import Response, status


async def add(dto: AddInstituteDTO):
    if await institute_repository.has_by_name(dto.name):
        raise InstituteAlreadyExistsException()
    
    await institute_repository.add(
        dto.name, 
        dto.short_name,
        dto.address
    )
    return Response(status_code=status.HTTP_201_CREATED)
