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
):
    filters = []

    if rating_start is not None and rating_start != -1:
        filters.append(Subject.rating >= rating_start)

    if rating_end is not None and rating_end != -1:
        filters.append(Subject.rating <= rating_end)
        
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