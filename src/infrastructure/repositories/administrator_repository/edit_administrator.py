from src.infrastructure.database import Administrator, update_instance

from uuid import UUID


async def update_by_id(admin_id: UUID, dto: dict):
    return await update_instance(Administrator, admin_id, dto)
