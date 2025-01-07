from src.infrastructure.enums.role import Role
from src.infrastructure.repositories.auth_repository import (
    get_admin_password_by_email, get_teacher_password_by_email
)


async def get_user_password_and_id_by_email_and_role(email: str, role: Role) -> str:
    """
    Gets user data depending on role
    """
    if role == Role.TEACHER:
        return await get_teacher_password_by_email(email)
    return await get_admin_password_by_email(email)
