from src.infrastructure.database import Lesson, delete_from_instance_by_id

from uuid import UUID


async def delete_by_id(lesson_id: UUID):
    return await delete_from_instance_by_id(Lesson, lesson_id)
