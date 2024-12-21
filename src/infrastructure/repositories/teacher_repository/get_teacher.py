from src.infrastructure.database.extensions import user_to_save_dict
from src.infrastructure.database import Teacher, get



async def get_all(page, limit, columns, sort, search, desc, filters = None):
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


async def get_by_id(teacher_id: int) -> dict: 
    return user_to_save_dict(await get.get_by_id(Teacher, teacher_id))
