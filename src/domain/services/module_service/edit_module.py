from src.application.dto.module import EditModuleDTO
from src.infrastructure.repositories import module_repository
from src.infrastructure.exceptions import ModuleNotFoundException

from fastapi import Response, status
from uuid import UUID


async def edit(module_id: UUID, dto: EditModuleDTO):
    if not await module_repository.has_by_id(module_id):
        raise ModuleNotFoundException()
    
    dto = dto.model_dump(exclude_none=True)

    await module_repository.update_by_id(module_id, dto)
    return Response(status_code=status.HTTP_200_OK)


