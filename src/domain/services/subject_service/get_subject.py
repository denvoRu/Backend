from src.infrastructure.repositories import subject_repository
from src.infrastructure.exceptions import (
    SubjectNotFoundException,
    InvalidParametersException
)

from uuid import UUID


async def get_all(
    page, 
    limit, 
    columns, 
    sort, 
    search, 
    desc, 
    teacher_ids, 
    module_id, 
    not_in_module_by_id,
    subject_without_teacher_by_id,
    not_has_const_link_by_teacher_id
):
    """
    Gets all subjects
    :param page: page number
    :param limit: count of subjects
    :param columns: fields to return
    :param sort: field to sort
    :param search: search string
    :param desc: sort direction
    :param teacher_ids: teacher ids
    :param module_id: module id
    :param not_in_module_by_id: is subject in module
    :param subject_without_teacher_by_id: subject without teacher
    """
    if teacher_ids is not None:
        teacher_ids = teacher_ids.split(",")

    if search is not None and search != "":
        search = "name*{0}".format(search)
    
    try:
        return await subject_repository.get_all(
            page, 
            limit, 
            columns, 
            sort, 
            search, 
            desc, 
            teacher_ids, 
            module_id,
            not_in_module_by_id,
            subject_without_teacher_by_id,
            not_has_const_link_by_teacher_id
        )
    except Exception:
        raise InvalidParametersException()


async def get_by_id(subject_id: UUID):
    if not await subject_repository.has_by_id(subject_id):
        raise SubjectNotFoundException()
    
    return await subject_repository.get_by_id(subject_id)