from src.infrastructure.database import Module, get


async def get_all(page, limit, columns, sort, search, desc):
    return await get.get_all(Module, page, limit, columns, sort, search, desc)


async def get_by_id(module_id: int):
    return await get.get_by_id(Module, module_id)
