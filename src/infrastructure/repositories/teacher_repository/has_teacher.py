from src.infrastructure.database import Teacher, has_instance


async def has_by_id(teacher_id: int) -> bool:
    return await has_instance(Teacher, Teacher.id == teacher_id)
