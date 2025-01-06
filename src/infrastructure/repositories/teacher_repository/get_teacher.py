from src.infrastructure.database.extensions import user_to_save_dict
from src.infrastructure.repositories import study_group_repository
from src.infrastructure.database import Teacher, StudyGroup, get

from sqlalchemy import select, not_, or_, func
from uuid import UUID


async def get_all(
    page, 
    limit, 
    columns, 
    sort, 
    search, 
    desc, 
    rating_start, 
    rating_end, 
    subject_ids,
    filters = None,
    *,
    not_in_subject_by_id: UUID = None
):
    filters = filters if filters is not None else []

    if rating_start is not None and rating_start != -1:
        filters.append(Teacher.rating >= rating_start)

    if rating_end is not None and rating_end != -1:
        filters.append(Teacher.rating <= rating_end)

    if subject_ids is not None and len(subject_ids) > 0:
        filters.append(Teacher.id.in_(subject_ids))

    if not_in_subject_by_id is not None:
        filters.append(
                not_(Teacher.id.in_(
                    study_group_repository.stmt_get_by_id(
                        Teacher.id,
                        not_in_subject_by_id
                    )
                )
            )
        )

    if search is not None: 
        name_split = search.lower().split()
        filters.append(
            or_(
                func.lower(Teacher.first_name).in_(name_split), 
                func.lower(Teacher.second_name).in_(name_split), 
                func.lower(Teacher.third_name).in_(name_split)
            )
        )
        search = None

    result = await get.get_all(
        Teacher, 
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc,
        filters
    )
    return result


async def get_by_study_group(subject_id, page, limit, columns, sort, search, desc):
    stmt = select(StudyGroup.teacher_id).where(
        StudyGroup.subject_id == subject_id,
        StudyGroup.is_disabled == False
    )
    
    return await get_all(
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc, 
        None,
        None,
        None,
        [Teacher.id.in_(stmt)]
    )


async def get_by_id(teacher_id: UUID) -> dict: 
    return user_to_save_dict(
        await get.get_by_id(Teacher, teacher_id), 
        include=["institute_id", "rating"]
    )
