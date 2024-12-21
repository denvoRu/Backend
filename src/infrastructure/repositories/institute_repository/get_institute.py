from src.infrastructure.database import Institute, get


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


async def get_by_id(institute_id: int):
    return await get.get_by_id(Institute, institute_id)
