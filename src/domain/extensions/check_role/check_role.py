from src.domain.extensions.get_current_user import get_current_user
from src.infrastructure.enums.role import Role
from .user import User

from fastapi import Depends, HTTPException, status
from typing_extensions import Annotated


CurrentUser = Annotated[User, Depends(get_current_user)]


class RoleChecker:
    @staticmethod
    def __create_role_checker(role: Role):
        def get_current_active_user(
            current_user: CurrentUser,
        ):
            if current_user.role != role:
                raise HTTPException(
                    status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
                    detail=f"You are not {role.lower()}, you are {current_user.role.lower()}"
                )
            return current_user
    
        return get_current_active_user
    
    @staticmethod
    async def teacher(
        current_user: CurrentUser,
    ):
        func = RoleChecker.__create_role_checker(Role.TEACHER)
        return func(current_user)

    @staticmethod
    async def admin(current_user: CurrentUser):
        func = RoleChecker.__create_role_checker(Role.ADMIN)
        return func(current_user)
