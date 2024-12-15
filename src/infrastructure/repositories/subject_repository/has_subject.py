from src.infrastructure.database import has, Subject


async def has_by_id(subject_id: int):
    return await has.has_instance(Subject, Subject.id == subject_id)

async def has_by_name(name: int):
    return await has.has_instance(Subject, Subject.name == name)