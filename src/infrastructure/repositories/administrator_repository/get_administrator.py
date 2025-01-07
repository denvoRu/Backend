from src.infrastructure.database.extensions import user_to_save_dict
from src.infrastructure.database import Administrator, get


async def get_all(page, limit, columns, sort, search, desc):
    """
    Gets all administrators
    :param page: page number
    :param limit: count of administrators
    :param columns: columns to return
    :param sort: column to sort by
    :param search: search string
    :param desc: sort direction
    :return: list of administrators
    """
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
    