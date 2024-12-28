from src.infrastructure.database.extensions import user_to_save_dict
from src.infrastructure.database import Teacher, StudyGroup, get

from sqlalchemy import select
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
    filters = []
    ):
    filters = []
    
    if rating_start is not None and rating_start != -1:
        filters.append(Teacher.rating >= rating_start)

    if rating_end is not None and rating_end != -1:
        filters.append(Teacher.rating <= rating_end)

    if subject_ids is not None and len(subject_ids) > 0:
        filters.append(Teacher.id.in_(subject_ids))

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
    stmt = select(StudyGroup.teacher_id).where(StudyGroup.subject_id == subject_id)
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
        include=["institute_id"]
    )
