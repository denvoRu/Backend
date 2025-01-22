from src.infrastructure.exceptions.helpers import one_or_more

from fastapi.exceptions import HTTPException
from fastapi import status


class InvalidParametersException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=one_or_more("parameters are invalid.", True)
        )
