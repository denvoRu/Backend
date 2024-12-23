from src.infrastructure.database import Administrator, update

from uuid import UUID


async def update_by_id(admin_id: UUID, dto: dict):
    data = dto.model_dump(exclude_none=True)
    await update.update_instance(Administrator, admin_id, data)
