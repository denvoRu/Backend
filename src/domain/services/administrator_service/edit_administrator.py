from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import administrator_repository
from src.infrastructure.exceptions import AdministratorNotFoundException

from fastapi import Response, status
from bcrypt import gensalt, hashpw
from uuid import UUID

"""
All methods use repository's code and raise exceptions if something's wrong
"""


async def edit(admin_id: UUID, dto: EditUserDTO):
    if not await administrator_repository.has_by_id(admin_id):
        raise AdministratorNotFoundException()

    # edit logic - we create a dto_dict to give it to update method
    salt = gensalt()
    dto.password = hashpw(dto.password.encode(), salt).decode()
    dto_dict = dto.model_dump(exclude_none=True)

    await administrator_repository.update_by_id(admin_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)