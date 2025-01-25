from src.application.dto.institute import CreateInstituteDTO
from src.infrastructure.repositories import institute_repository
from src.infrastructure.exceptions import InstituteAlreadyExistsException

from fastapi import Response, status


async def add(dto: CreateInstituteDTO):
    if await institute_repository.has_by_name(dto.name):
        raise InstituteAlreadyExistsException()
    
    await institute_repository.add(
        dto.name, 
        dto.short_name,
        dto.address
    )
    return Response(status_code=status.HTTP_201_CREATED)
