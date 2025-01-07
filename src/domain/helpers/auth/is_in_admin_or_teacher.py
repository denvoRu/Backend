from src.infrastructure.enums.role import Role
from src.infrastructure.database.models.administrator import Administrator
from src.infrastructure.database.models.teacher import Teacher
from src.infrastructure.repositories.auth_repository.auth import is_in_table


async def is_in_teacher_or_admin(email: str, role: Role) -> bool:
    """
    Checks that current email is in table depending on role
    """
    if role == Role.TEACHER:
        return await is_in_table(Teacher, email)
    return await is_in_table(Administrator, email)
