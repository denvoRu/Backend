from src.infrastructure.database import Subject, has_instance

from uuid import UUID


async def has_by_id(subject_id: UUID):
    return await has_instance(Subject, Subject.id == subject_id)

async def has_by_name(name: int):
    return await has_instance(Subject, Subject.name == name)
