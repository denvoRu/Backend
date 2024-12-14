from src.infrastructure.database import delete_user, Teacher

async def delete_teacher(teacher_id: int):
    return await delete_user(teacher_id, Teacher)
        