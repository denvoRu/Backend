from src.infrastructure.repositories import administrator_repository
from src.infrastructure.exceptions import (
    AdministratorNotFoundException,
    InvalidParametersException
)


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
