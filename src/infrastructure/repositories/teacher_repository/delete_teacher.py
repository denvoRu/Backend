from src.infrastructure.database import Teacher, delete_from_instance_by_id

from uuid import UUID

async def delete_by_id(teacher_id: UUID):
    return await delete_from_instance_by_id(Teacher, teacher_id)
    