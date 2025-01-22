from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import administrator_repository
from src.infrastructure.exceptions import (
    AdministratorNotFoundException, 
    InvalidParametersException
)

from fastapi import Response, status
from bcrypt import gensalt, hashpw
from uuid import UUID

"""
All methods use repository's code and raise exceptions if something's wrong
"""


async def get_all(page, limit, columns, sort, search, desc):
    try:
        return await administrator_repository.get_all(
            page, limit, columns, sort, search, desc
        )
    except Exception:
        raise InvalidParametersException()


async def get_by_id(admin_id: str):
    if not await administrator_repository.has_by_id(admin_id):
        raise AdministratorNotFoundException()

    return await administrator_repository.get_by_id(admin_id)


async def edit(admin_id: UUID, dto: EditUserDTO):
    if not await administrator_repository.has_by_id(admin_id):
        raise AdministratorNotFoundException()

    # edit logic - we create a dto_dict to give it to update method
    salt = gensalt()
    dto.password = hashpw(dto.password.encode(), salt).decode()
    dto_dict = dto.model_dump(exclude_none=True)

    await administrator_repository.update_by_id(admin_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)


async def delete(admin_id: str):
    if not await administrator_repository.has_by_id(admin_id):
        raise AdministratorNotFoundException()

    await administrator_repository.delete_by_id(admin_id)
    return Response(status_code=status.HTTP_200_OK)
