from src.infrastructure.database import (
    get, Teacher
)
from typing import List


async def get_by_email(email: str,) -> dict:
    return await get.get_by_email(email, Teacher)
    
async def all() -> List[dict]:
    return await get.get_all(Teacher)
    
async def get_by_id(teacher_id: int) -> dict: ...
