from domain.enums.role import Role
from infrastructure.repositories.auth_repository import (
    get_admin_by_email, get_teacher_by_email
)


def get_user_password_by_email_and_role(email: str, role: Role) -> str:
    if role == Role.TEACHER:
        return get_teacher_by_email(email)
    return get_admin_by_email(email)