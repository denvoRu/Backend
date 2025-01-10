from src.infrastructure.models.page_response import PageResponse
from src.infrastructure.database import Module, Subject, StudyGroup, get, db
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
    institute_ids,
    teacher_ids
):
    """
    Gets all modules with subjects
    :param page: current page
    :param limit: limit of modules
    :param sort: field to sort
    :param search: search string
    :param desc: sort order
    :param rating_start: start of rating range
    :param rating_end: end of rating range
    :param institute_ids: institute ids
    :param teacher_ids: teacher ids
    """
    try:
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
        

        if rating_start is not None and rating_start != -1:
            module_filters.append(Module.rating >= rating_start)

        if rating_end is not None and rating_end != -1:
            module_filters.append(Module.rating <= rating_end)

        if institute_ids is not None and len(institute_ids) > 0:
            module_filters.append(Module.institute_id.in_(institute_ids))

        if teacher_ids is not None and len(teacher_ids) > 0:
            subject_filters.append(
                Subject.id.in_(
                    select(StudyGroup.subject_id)
                    .where(StudyGroup.teacher_id.in_(teacher_ids))
                )
            )
            module_filters.append(
                Module.id.in_(
                    select(Subject.module_id).select_from(StudyGroup).join(
                        Subject, StudyGroup.subject_id == Subject.id
                    ).where(StudyGroup.teacher_id.in_(teacher_ids))
                )
            )

        module_filters.append(Module.is_disabled == False)
        subject_filters.append(Subject.is_disabled == False)

        module_stmt = module_stmt.where(*module_filters)
        subject_stmt = select(Subject).where(*subject_filters)

        if sort is not None and sort != "":
            sorted_columns = map(text, sort.split(","))
            if desc == 1:
                sorted_columns = map(order_desc, sorted_columns)

            module_stmt = module_stmt.order_by(*sorted_columns)
        
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
    except Exception as e:
        await db.commit_rollback()
        raise Exception(str(e))


async def get_all(page, limit, columns, sort, search, desc, institute_id):
    """
    Gets all modules
    :param page: current page
    :param limit: limit of modules
    :param columns: columns to show
    :param sort: field to sort
    :param search: search string
    :param desc: sort order
    :param institute_id: institute id
    """
    filters = []

    if institute_id is not None:
        filters.append(Module.institute_id == institute_id)

    return await get.get_all(
        Module, 
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc,
        filters
    )


async def get_by_id(module_id: UUID):
    return await get.get_by_id(Module, module_id)
