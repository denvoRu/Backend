from src.infrastructure.database.extensions import user_to_save_dict
from src.infrastructure.database import Administrator, get


async def get_all(page, limit, columns, sort, search, desc):
    return await get.get_all(
        Administrator, 
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc
    )


async def get_by_id(admin_id: str,) -> dict:
    return user_to_save_dict(await get.get_by_id(Administrator, admin_id))
    