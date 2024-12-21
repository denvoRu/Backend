from src.infrastructure.enums.role import Role
from src.infrastructure.database import (
    Teacher, Administrator, update_instance
)


async def update_password(user_id: int, role: Role, password: str):
    instance = Teacher if role == Role.TEACHER else Administrator
    await update_instance(instance, user_id, {"password": password})
