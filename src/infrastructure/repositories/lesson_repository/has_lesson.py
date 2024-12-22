from src.infrastructure.database import Lesson, has_instance


async def has_by_id(lesson_id: int):
    return await has_instance(Lesson, Lesson.id == lesson_id)
