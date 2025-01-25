from src.infrastructure.exceptions import (
    InstituteNotFoundException, 
    ConstLinkNotFoundException,
    LessonNotFoundException
)
from src.infrastructure.repositories import (
    lesson_repository,
    study_group_repository,
    institute_repository,
)

from uuid import UUID


async def get_all(
    institute_id: UUID,
    page: int = 1,
    limit: int = 10,
    search: str = None,
):
    if not await institute_repository.has_by_id(institute_id):
        raise InstituteNotFoundException()
    
    return await study_group_repository.get_const_links(
        institute_id,
        page, 
        limit, 
        search, 
    )


async def get_active(const_link_id: UUID):
    try:
        if not await study_group_repository.has_end_date(const_link_id):
            raise ConstLinkNotFoundException()
        
        return await lesson_repository.get_active_by_const_link_id(
            const_link_id
        )
    except Exception:
        raise LessonNotFoundException()
