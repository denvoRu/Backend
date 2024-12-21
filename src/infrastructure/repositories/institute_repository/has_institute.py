from src.infrastructure.database import Institute, has_instance


async def has_by_name(institude_name: str):
    return await has_instance(Institute, Institute.name == institude_name)


async def has_by_id(institute_id: int):
    return await has_instance(Institute, Institute.id == institute_id)
