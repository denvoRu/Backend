from src.infrastructure.database import Administrator, has

from uuid import UUID


async def has_by_id(admin_id: UUID):
    # does administrator exist ?
    return await has.has_instance(
        Administrator, 
        Administrator.id == admin_id
    )
