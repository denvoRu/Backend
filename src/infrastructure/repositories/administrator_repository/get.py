from src.infrastructure.database.extensions import user_to_save_dict
from src.infrastructure.database import get, Administrator
from typing import List


async def get_by_id(admin_id: str,) -> dict:
    return user_to_save_dict(await get.get_by_id(admin_id, Administrator))
    
async def all(page, limit, columns, sort, filter, desc) -> List[dict]:
    return await get.get_all(Administrator, page, limit, columns, sort, filter, desc)
    
