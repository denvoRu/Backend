from src.infrastructure.database import Administrator, update


async def update_by_id(admin_id: int, dto: dict):
    data = dto.model_dump(exclude_none=True)
    await update.update_instance(Administrator, admin_id, data)
