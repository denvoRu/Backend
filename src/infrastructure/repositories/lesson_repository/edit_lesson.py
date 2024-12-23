from src.infrastructure.database import Lesson, update_instance

from uuid import UUID


async def update_by_id(lesson_id: UUID, dto: dict):
    return await update_instance(Lesson, lesson_id, dto)
