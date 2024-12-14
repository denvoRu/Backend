from src.infrastructure.database import delete, Administrator

async def delete_admin(admin_id: int):
    return await delete.delete_user(admin_id, Administrator)
        