from src.infrastructure.exceptions.helpers import in_

from fastapi.exceptions import HTTPException
from fastapi import status


class AlreadyExistsException(HTTPException):
    def __init__(self, name: str, in_name: str = None):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{name} already exists{' ' + in_(in_name)}."
        )
