from src.infrastructure.repositories import institute_repository
from src.infrastructure.exceptions import InstituteNotFoundException

from fastapi import Response, status
from uuid import UUID


async def delete(institute_id: UUID):
    if not await institute_repository.has_by_id(institute_id):
        raise InstituteNotFoundException()

    await institute_repository.delete_by_id(institute_id)
    return Response(status_code=status.HTTP_200_OK)
