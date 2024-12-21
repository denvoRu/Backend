from src.infrastructure.database import Administrator, has


async def has_by_id(admin_id: int):
    return await has.has_instance(
        Administrator, 
        Administrator.id == admin_id
    )
