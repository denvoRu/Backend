from src.infrastructure.database import Teacher, delete

from uuid import UUID

async def delete_by_id(teacher_id: UUID):
    return await delete.delete_from_instance_by_id(Teacher, teacher_id)
    