from src.application.dto.module import CreateModuleDTO
from src.infrastructure.repositories import module_repository
from src.infrastructure.exceptions import ModuleAlreadyExistsException

from fastapi import Response, status


async def add(dto: CreateModuleDTO): 
    if await module_repository.has_by_name(dto.name):
        raise ModuleAlreadyExistsException()
    
    await module_repository.add(dto.institute_id, dto.name)
    return Response(status_code=status.HTTP_201_CREATED)
