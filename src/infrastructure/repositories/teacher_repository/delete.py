from src.infrastructure.database import delete, Teacher

async def delete_teacher(teacher_id: int):
    return await delete.delete_from_instance_by_id(Teacher, teacher_id)
        