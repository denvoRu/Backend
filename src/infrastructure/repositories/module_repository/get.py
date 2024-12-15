from src.infrastructure.database import get, Module

async def get_by_id(module_id: int) -> Module:
    return await get.get_by_id(Module, module_id)

async def get_all(page, limit, columns, sort, search, desc):
    return await get.get_all(Module, page, limit, columns, sort, search, desc)