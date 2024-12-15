from src.infrastructure.database import delete, Administrator

async def delete_admin(admin_id: int):
    return await delete.delete_from_instance_by_id(Administrator, admin_id)
        