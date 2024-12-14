from src.infrastructure.database import delete_user, Administrator

async def delete_admin(admin_id: int):
    return await delete_user(admin_id, Administrator)
        