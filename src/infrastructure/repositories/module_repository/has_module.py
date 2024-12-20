from src.infrastructure.database import has_instance, Module


async def has_by_id(module_id: int):
    return await has_instance(Module, Module.id == module_id)


async def has_by_name(name: int):
    return await has_instance(Module, Module.name == name)