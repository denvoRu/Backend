from src.infrastructure.database import Teacher, delete


async def delete_by_id(teacher_id: int):
    return await delete.delete_from_instance_by_id(Teacher, teacher_id)
    