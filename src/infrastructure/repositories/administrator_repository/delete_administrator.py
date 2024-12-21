from src.infrastructure.database import Administrator, delete


async def delete_by_id(admin_id: int):
    return await delete.delete_from_instance_by_id(Administrator, admin_id)
