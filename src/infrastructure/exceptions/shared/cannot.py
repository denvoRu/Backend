from fastapi.exceptions import HTTPException
from fastapi import status


class CannotException(HTTPException):
    def __init__(self, s: str):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"You cannot {s.lower()}."
        )
