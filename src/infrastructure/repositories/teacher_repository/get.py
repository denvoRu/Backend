from src.infrastructure.database import get, Teacher
from typing import List

async def all(page, limit, columns, sort, filter) -> List[dict]:
    result = await get.get_all(Teacher, page, limit, columns, sort, filter)
    print(result)
    return result
    
async def get_by_id(teacher_id: int) -> dict: 
    return await get.get_by_id(teacher_id, Teacher)