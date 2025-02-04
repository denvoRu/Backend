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
    institute_ids = None,
    not_in_subject_by_id: UUID = None
):
    """
    Gets all teachers
    :param page: current page
    :param limit: number of teachers to show
    :param columns: columns to show
    :param sort: field to sort by
    :param search: search string
    :param desc: sort direction
    :param rating_start: start rating for filter
    :param rating_end: end rating for filter
    :param subject_ids: subject ids
    :param filters: filters
    """
    filters = filters if filters is not None else []

    if rating_start is not None and rating_start != -1:
        filters.append(Teacher.rating >= rating_start)

    if rating_end is not None and rating_end != -1:
        filters.append(Teacher.rating <= rating_end)

    if subject_ids is not None and len(subject_ids) > 0:
        study_groups_ids_stmt = select(StudyGroup.teacher_id).where(
            StudyGroup.subject_id.in_(subject_ids)
        )
        filters.append(Teacher.id.in_(study_groups_ids_stmt))

    if institute_ids is not None and len(institute_ids) > 0:
        filters.append(Teacher.institute_id.in_(institute_ids))

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
                *[func.lower(j).like(f"%{i}%") for i in name_split
                for j in (
                    Teacher.first_name, 
                    Teacher.second_name, 
                    Teacher.third_name
                )]
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


async def get_by_study_group(
    subject_id, 
    page, 
    limit, 
    columns, 
    sort, 
    search, 
    desc,
    not_has_const_link
):
    """
    Gets teachers by study group id
    :param subject_id: subject id
    :param page: current page
    :param limit: number of teachers to show
    :param columns: columns to show
    :param sort: field to sort by
    :param search: search string
    :param desc: sort direction
    """
    filters = []
    if not_has_const_link: 
        filters.append(StudyGroup.const_end_date == None)
        
    stmt = select(StudyGroup.teacher_id).where(
        StudyGroup.subject_id == subject_id,
        StudyGroup.is_disabled == False,
        *filters 
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


async def get_id_by_study_group(study_group_id: UUID) -> UUID:
    return await get.get_by_id(
        StudyGroup,
        study_group_id,
        attr_name="teacher_id"
    )
