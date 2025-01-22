from fastapi.exceptions import HTTPException
from fastapi import status


class IncorrectUsernameOrPasswordException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect username or password"
        )