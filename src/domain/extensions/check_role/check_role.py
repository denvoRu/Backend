from src.domain.extensions.get_current_user import get_current_user
from src.infrastructure.enums.role import Role
from src.infrastructure.exceptions import RoleMatchException
from .user import User

from fastapi import Depends
from typing_extensions import Annotated


CurrentUser = Annotated[User, Depends(get_current_user)]


class RoleChecker:
    @staticmethod
    def __create_role_checker(role: Role):
        """
        Checks the role of user: is it administrator or teacher
        :param role: needed role
        :return: current user if role is validated
        """
        def get_current_active_user(
            current_user: CurrentUser,
        ):
            if current_user.role != role:
                raise RoleMatchException(current_user.role, role)
            return current_user
    
        return get_current_active_user

    # checker for teacher
    @staticmethod
    async def teacher(
        current_user: CurrentUser,
    ):
        func = RoleChecker.__create_role_checker(Role.TEACHER)
        return func(current_user)

    # checker for admin
    @staticmethod
    async def admin(current_user: CurrentUser):
        func = RoleChecker.__create_role_checker(Role.ADMIN)
        return func(current_user)
