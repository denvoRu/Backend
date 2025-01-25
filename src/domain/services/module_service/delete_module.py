
from src.infrastructure.repositories import module_repository
from src.infrastructure.exceptions import ModuleNotFoundException

from fastapi import Response, status
from uuid import UUID


async def delete(module_id: UUID):
    if not await module_repository.has_by_id(module_id):
        raise ModuleNotFoundException()
    
    await module_repository.delete_by_id(module_id)
    return Response(status_code=status.HTTP_200_OK)
