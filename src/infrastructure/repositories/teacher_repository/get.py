from src.infrastructure.database.extensions import user_to_save_dict
from src.infrastructure.database import get, Teacher
from typing import List

async def all(page, limit, columns, sort, filter, desc) -> List[dict]:
    result = await get.get_all(Teacher, page, limit, columns, sort, filter, desc)
    return result
    
async def get_by_id(teacher_id: int) -> dict: 
    return user_to_save_dict(await get.get_by_id(teacher_id, Teacher))