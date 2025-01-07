from src.infrastructure.enums.role import Role
from src.infrastructure.database import (
    Teacher, Administrator, update_instance
)

from uuid import UUID


async def update_password(user_id: UUID, role: Role, password: str):
    """
    Updates the password for the given user depending on role.
    """
    instance = Teacher if role == Role.TEACHER else Administrator
    await update_instance(instance, user_id, {"password": password})
