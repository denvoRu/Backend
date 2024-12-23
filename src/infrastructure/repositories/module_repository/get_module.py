from src.infrastructure.database import Module, get

from uuid import UUID


async def get_all(page, limit, columns, sort, search, desc, institute_id):
    filters = []
    if institute_id is not None:
        filters.append(Module.institute_id == institute_id)
    return await get.get_all(Module, page, limit, columns, sort, search, desc)


async def get_by_id(module_id: UUID):
    return await get.get_by_id(Module, module_id)
