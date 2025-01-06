from src.infrastructure.repositories.study_group_repository import (
    get_subject_ids_by_teacher_statement
)
from .stmt import stmt_get_by_module_id
from src.infrastructure.database import Subject, get

from sqlalchemy import not_
from uuid import UUID


async def get_all(
    page, 
    limit, 
    columns, 
    sort, 
    search, 
    desc, 
    teacher_ids = [],
    module_id = None,
    not_in_module_by_id: UUID = None
):
    filters = []
    
    if module_id is not None:
        filters.append(Subject.module_id == module_id)

    if teacher_ids is not None and len(teacher_ids) > 0:
        subject_ids = get_subject_ids_by_teacher_statement(teacher_ids)
        filters.append(Subject.id.in_(subject_ids))
    
    if not_in_module_by_id is not None:
        filters.append(
                not_(Subject.id.in_(
                    stmt_get_by_module_id(not_in_module_by_id)
                )
            )
        )
        
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


async def get_by_id(subject_id: UUID) -> Subject:
    return await get.get_by_id(Subject, subject_id)

