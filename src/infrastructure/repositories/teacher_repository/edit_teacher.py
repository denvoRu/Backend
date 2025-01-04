from src.infrastructure.database import Teacher, update_instance


async def update_by_id(user_id, dto: dict):
    await update_instance(Teacher, user_id, dto)
