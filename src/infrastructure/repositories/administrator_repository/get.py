from src.infrastructure.database import (
    get, Administrator
)
from typing import List


async def get_by_id(admin_id: str,) -> dict:
    return await get.get_by_id(admin_id, Administrator)
    
async def all(page, limit, columns, sort, filter) -> List[dict]:
    return await get.get_all(Administrator, page, limit, columns, sort, filter)
    
