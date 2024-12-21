from src.infrastructure.database import Teacher, update


async def update_by_id(user_id, dto: dict):
    await update.update_instance(Teacher, user_id, dto)
