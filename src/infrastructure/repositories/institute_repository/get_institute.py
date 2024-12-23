from src.infrastructure.database import Institute, get

from uuid import UUID


async def get_all(page, limit, columns, sort, search, desc):
    return await get.get_all(
        Institute,
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc
    )


async def get_by_id(institute_id: UUID):
    return await get.get_by_id(Institute, institute_id)
