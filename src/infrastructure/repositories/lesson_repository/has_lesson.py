from src.infrastructure.database import Lesson, has_instance

from uuid import UUID


async def has_by_id(lesson_id: UUID):
    return await has_instance(Lesson, Lesson.id == lesson_id)
