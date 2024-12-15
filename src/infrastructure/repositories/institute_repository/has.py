from src.infrastructure.database import Institute, has


async def has_institute(institude_name: str):
    return await has.has_instance(Institute, Institute.name == institude_name)

async def has_institute_by_id(institute_id: int):
    return await has.has_instance(Institute, Institute.id == institute_id)