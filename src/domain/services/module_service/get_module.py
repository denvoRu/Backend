from src.infrastructure.repositories import module_repository
from src.infrastructure.exceptions import (
    ModuleNotFoundException,
    InvalidParametersException,
)

from uuid import UUID


async def get_all_with_subjects(
    page, 
    limit, 
    sort, 
    search, 
    desc, 
    rating_start, 
    rating_end, 
    institute_ids,
    teacher_ids
):
    """
    Returns all modules with subjects
    :param page: current page
    :param limit: number of modules to return
    :param sort: sort order
    :param search: search string
    :param desc: sort direction
    :param rating_start: start of rating range
    :param rating_end: end of rating range
    :param institute_ids: institute ids to find
    :param teacher_ids: teacher ids to find
    """
    if institute_ids is not None:
        institute_ids = institute_ids.split(",")
        
    if teacher_ids is not None:
        teacher_ids = teacher_ids.split(",")
        
    try: 
        return await module_repository.get_all_with_subjects(
            page, 
            limit, 
            sort, 
            search, 
            desc, 
            rating_start, 
            rating_end, 
            institute_ids,
            teacher_ids
        )
    except Exception:
        raise InvalidParametersException()


async def get_all(
    page, 
    limit, 
    columns, 
    sort, 
    search, 
    desc, 
    institute_id
):
    """
    Returns all modules
    :param page: current page
    :param limit: number of modules to return
    :param columns: fields to show
    :param sort: sort order
    :param search: search string
    :param desc: sort direction
    :param institute_id: institute id to find
    """
    if search is not None and search != "":
        search = "name*{0}".format(search)

    try:
        return await module_repository.get_all(
            page, 
            limit, 
            columns, 
            sort, 
            search, 
            desc, 
            institute_id
        )
    except Exception:
        raise InvalidParametersException()


async def get_by_id(module_id: UUID): 
    if not await module_repository.has_by_id(module_id):
        raise ModuleNotFoundException()
    
    return await module_repository.get_by_id(module_id)
