from .stmt import stmt_get_by_module_id
from src.infrastructure.database import Subject, get
from src.infrastructure.repositories.study_group_repository import (
    get_subject_ids_by_teacher_statement
)

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
    not_in_module_by_id: UUID = None,
    subject_without_teacher_by_id: UUID = None,
    not_has_const_link_by_teacher_id: UUID = None
):
    """
    Gets all subjects
    :param page: current page
    :param limit: limit of subjects to show
    :param columns: fields to show
    :param sort: field sort
    :param search: search string
    :param desc: sort order
    :param teacher_ids: teacher ids
    :param module_id: module id
    :param not_in_module_by_id: is subject NOT in module
    :param subject_without_teacher_by_id: subject without teacher
    """
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

    if subject_without_teacher_by_id is not None:
        filters.append(
                not_(Subject.id.in_(
                    get_subject_ids_by_teacher_statement([subject_without_teacher_by_id])
                )
            )
        )
    
    if not_has_const_link_by_teacher_id:
        filters.append(Subject.id.in_(
            get_subject_ids_by_teacher_statement(
                [not_has_const_link_by_teacher_id], 
                True
            )
        ))
        
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
