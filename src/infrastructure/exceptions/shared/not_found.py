from src.infrastructure.exceptions.helpers import in_, one_or_more

from enum import Enum
from fastapi.exceptions import HTTPException
from fastapi import status


class NotFoundException(HTTPException):
    def __init__(self, name: Enum, in_name: Enum = None, has_one_or_more: bool = False):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=one_or_more(
                f"{name.value} not found{' ' + in_(in_name.value)}.", 
                has_one_or_more
            )
        )
