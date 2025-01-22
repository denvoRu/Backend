from typing import Generic, List, TypeVar
from pydantic.generics import GenericModel


T = TypeVar("T")


class PageResponse(GenericModel, Generic[T]):
    """ 
    The response for a pagination query
    """
    page_number: int
    page_size: int
    total_pages: int
    total_record: int
    content: List[T]
