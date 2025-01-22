from fastapi.exceptions import HTTPException
from fastapi import status


class NotValidateCredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Could not validate credentials", 
            headers={"WWW-Authenticate": "Bearer"}
        )