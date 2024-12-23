from src.infrastructure.database import Module, Subject, get, db
from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.models.module_with_subject_response import (
    ModuleWithSubjectResponse
)

from sqlalchemy import select, desc as order_desc, text, func, or_
from uuid import UUID
from math import ceil


async def get_all_with_subjects(
    page, 
    limit, 
    sort, 
    search, 
    desc, 
    rating_start, 
    rating_end, 
    institute_ids
):
    module_stmt = select(Module)
    module_filters = []
    subject_filters = []

    if search is not None and search != "":
        search_lower = search.lower()
        module_name_filter = func.lower(Module.name).contains(search_lower)
        subject_name_filter = func.lower(Subject.name).contains(search_lower)

        subject_module_ids = select(Subject.module_id).where(subject_name_filter)
        module_ids = select(Module.id).where(module_name_filter)

        select_subjects = select(Subject.id).where(subject_name_filter)
        select_modules = select(Subject.id).where(Subject.module_id.in_(module_ids))
        
        subject_filters.append(
            or_(
                Subject.id.in_(select_subjects),
                Subject.id.in_(select_modules)
            )
        )
        module_filters.append(
            or_(
                Module.id.in_(subject_module_ids),
                Module.id.in_(module_ids)
            )
        )
    
    if sort is not None and sort != "":
        sorted_columns = map(text, sort.split(","))
        if desc == 1:
            sorted_columns = map(order_desc, sorted_columns)

        module_stmt.order_by(sorted_columns)

    if rating_start is not None and rating_start != -1:
        module_filters.append(Module.rating >= rating_start)

    if rating_end is not None and rating_end != -1:
        module_filters.append(Module.rating <= rating_end)

    if institute_ids is not None and len(institute_ids) > 0:
        module_filters.append(Module.institute_id.in_(institute_ids))

    module_stmt = module_stmt.where(
        *module_filters
    )

    subject_stmt = select(Subject).where(
        *subject_filters
    )
    
    # count query
    count_query = select(func.count(1)).select_from(module_stmt)
    total_record = (await db.execute(count_query)).scalar() or 0
    
    module_stmt = module_stmt.offset((page - 1) * limit).limit(limit)

    modules = await db.execute(module_stmt)
    modules = modules.scalars().all()

    subjects = await db.execute(subject_stmt)
    subjects = subjects.scalars().all()

    module_with_subjects = ModuleWithSubjectResponse(modules, subjects) 
    total_page = ceil(total_record / limit)

    return PageResponse(
        page_number=page,
        page_size=limit,
        total_pages=total_page,
        total_record=total_record,
        content=module_with_subjects.to_dict()
    )

async def get_all(page, limit, columns, sort, search, desc):
    return await get.get_all(
        Module, 
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc
    )


async def get_by_id(module_id: UUID):
    return await get.get_by_id(Module, module_id)
