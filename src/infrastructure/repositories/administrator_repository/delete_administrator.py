from src.infrastructure.database import Administrator, delete_from_instance_by_id

from uuid import UUID


async def delete_by_id(admin_id: UUID):
    return await delete_from_instance_by_id(Administrator, admin_id)
