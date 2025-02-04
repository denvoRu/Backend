from src.infrastructure.exceptions.helpers import in_, one_or_more

from enum import Enum
from fastapi.exceptions import HTTPException
from fastapi import status


class NotFoundException(HTTPException):
    def __init__(self, name: Enum, in_name: Enum = None, has_one_or_more: bool = False):
        end_str = ' ' + in_(in_name.value) if in_name is not None else ''
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=one_or_more(
                f"{name.value} not found{end_str}.", 
                has_one_or_more
            )
        )
