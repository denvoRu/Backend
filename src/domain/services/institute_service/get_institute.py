from src.infrastructure.repositories import institute_repository
from src.infrastructure.exceptions import (
    InstituteNotFoundException,
    InvalidParametersException
)

from uuid import UUID


async def get_all(page, limit, columns, sort, search, desc):
    """
    Gets all institutes with needed filters
    :param page: page number
    :param limit: count of results to return
    :param columns: fields to return
    :param sort: field to sort by
    :param search: search string
    :param desc: sort direction
    """
    if search is not None and search != "":
        search = "name*{0},short_name*{0}".format(search)
        
    try: 
        return await institute_repository.get_all(
            page, 
            limit, 
            columns, 
            sort, 
            search, 
            desc
        )
    except Exception:
        raise InvalidParametersException()


async def get_by_id(institute_id: UUID):
    if not await institute_repository.has_by_id(institute_id):
        raise InstituteNotFoundException()
 
    return await institute_repository.get_by_id(institute_id)
