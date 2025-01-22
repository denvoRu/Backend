from src.infrastructure.enums.role import Role

from fastapi.exceptions import HTTPException
from fastapi import status


class RoleMatchException(HTTPException):
    def __init__(self, current_role: Role, required_role: Role):
        super().__init__(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
            detail=f"You are not {required_role.lower()}, you are {current_role.lower()}"
        )