from src.infrastructure.exceptions.helpers import to_many_form
from src.infrastructure.exceptions.shared import Names

from fastapi.exceptions import HTTPException
from fastapi import status


class NotHaveEnoughPrivilegesException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_405_METHOD_NOT_ALLOWED, 
            detail=f"You don't have enough {to_many_form(Names.PRIVILEGE)}"
        )