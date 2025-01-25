from src.infrastructure.exceptions import SubjectNotFoundException
from src.infrastructure.repositories import (
    subject_repository,
    teacher_repository
)


async def get_teachers(
    subject_id, 
    page: int = 1, 
    limit: int = 10, 
    columns: str = None, 
    sort: str = None, 
    search: str = None, 
    desc: int = 0,
    not_has_const_link = False
):
    """
    Get all teachers from study group
    :param subject_id: id of subject
    :param page: page number
    :param limit: count of teachers to show
    :param columns: fields to show
    :param sort: sort order
    :param search: search string
    :param desc: descending order
    """
    if not await subject_repository.has_by_id(subject_id):
        raise SubjectNotFoundException()
    
    return await teacher_repository.get_by_study_group(
        subject_id, 
        page, 
        limit, 
        columns,
        sort, 
        search, 
        desc,
        not_has_const_link
    )