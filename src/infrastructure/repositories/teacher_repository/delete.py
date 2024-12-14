from src.infrastructure.database import delete, Teacher

async def delete_teacher(teacher_id: int):
    return await delete.delete_user(teacher_id, Teacher)
        