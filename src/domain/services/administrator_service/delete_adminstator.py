from src.infrastructure.repositories import administrator_repository
from src.infrastructure.exceptions import AdministratorNotFoundException

from fastapi import Response, status

"""
All methods use repository's code and raise exceptions if something's wrong
"""


async def delete(admin_id: str):
    if not await administrator_repository.has_by_id(admin_id):
        raise AdministratorNotFoundException()

    await administrator_repository.delete_by_id(admin_id)
    return Response(status_code=status.HTTP_200_OK)
