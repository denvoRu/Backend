from src.infrastructure.database import (
    get, Teacher
)
from typing import List

async def all() -> List[dict]:
    return await get.get_all(Teacher)
    
async def get_by_id(teacher_id: int) -> dict: 
    return await get.get_by_id(teacher_id, Teacher)