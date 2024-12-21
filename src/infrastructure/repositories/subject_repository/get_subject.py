from src.infrastructure.repositories.study_group_repository import (
    get_subject_ids_by_teacher_statement
)
from src.infrastructure.database import get, Subject


async def get_by_id(subject_id: int) -> Subject:
    return await get.get_by_id(Subject, subject_id)


async def get_all(
    page, 
    limit, 
    columns, 
    sort, 
    search, 
    desc, 
    rating_start = -1, 
    rating_end = -1,
    teacher_ids = [],
    module_id = None
):
    filters = []

    if rating_start is not None and rating_start != -1:
        filters.append(Subject.rating >= rating_start)

    if rating_end is not None and rating_end != -1:
        filters.append(Subject.rating <= rating_end)

    if module_id is not None:
        filters.append(Subject.module_id == module_id)

    if teacher_ids is not None and len(teacher_ids) > 0:
        subject_ids = get_subject_ids_by_teacher_statement(teacher_ids)
        filters.append(Subject.id.in_(subject_ids))
        
    return await get.get_all(
        Subject, 
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc,
        filters
    )