from typing import List
from src.infrastructure.database import get, Institute


async def get_institute(institute_id: int) -> Institute:
    return await get.get_by_id(Institute, institute_id)


async def get_all_institutes(
    page, limit, columns, sort, search, desc
) -> List[dict]:
    return await get.get_all(
        Institute,
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc
    )


