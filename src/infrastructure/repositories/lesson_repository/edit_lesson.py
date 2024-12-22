from src.infrastructure.database import Lesson, update_instance


async def update_by_id(lesson_id: int, dto: dict):
    return await update_instance(Lesson, lesson_id, dto)
