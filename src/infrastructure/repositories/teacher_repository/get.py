from src.infrastructure.database import (
    get, Teacher
)
from typing import List

async def all(page, limit, columns, sort, filter) -> List[dict]:
    return await get.get_all(Teacher, page, limit, columns, sort, filter)
    
async def get_by_id(teacher_id: int) -> dict: 
    return await get.get_by_id(teacher_id, Teacher)