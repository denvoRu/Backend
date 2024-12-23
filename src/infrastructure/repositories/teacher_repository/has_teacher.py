from src.infrastructure.database import Teacher, has_instance

from uuid import UUID


async def has_by_id(teacher_id: UUID) -> bool:
    return await has_instance(Teacher, Teacher.id == teacher_id)
