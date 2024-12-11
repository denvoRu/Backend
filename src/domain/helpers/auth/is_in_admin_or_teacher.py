from src.domain.enums.role import Role
from src.infrastructure.database.models.administrator import Administrator
from src.infrastructure.database.models.teacher import Teacher
from src.infrastructure.repositories.auth_repository.auth import is_in_table


def is_in_teacher_or_admin(email: str, role: Role) -> bool:
    if role == Role.TEACHER:
        return is_in_table(Teacher, email)
    return is_in_table(Administrator, email)