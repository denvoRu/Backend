from fastapi.exceptions import HTTPException
from fastapi import status


class RequiredException(HTTPException):
    def __init__(self, name: str, has_is: bool = True, has_are: bool = False):
        is_or_are = "is" if has_is and not has_are else "are"
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{name} {is_or_are} required."
        )
