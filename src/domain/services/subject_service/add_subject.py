from src.application.dto.subject import AddSubjectDTO
from src.infrastructure.repositories import (
    subject_repository, 
    module_repository
)
from src.infrastructure.exceptions import (
    ModuleNotFoundException,
    SubjectAlreadyExistsException
)

from fastapi import Response, status
    

async def add(dto: AddSubjectDTO):
    if await subject_repository.has_by_name(dto.name):
        raise SubjectAlreadyExistsException()
    
    if not await module_repository.has_by_id(dto.module_id):
        raise ModuleNotFoundException
 
    await subject_repository.add(dto.module_id, dto.name)
    return Response(status_code=status.HTTP_201_CREATED)
