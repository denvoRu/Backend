from src.infrastructure.database import Lesson, add_instance


async def add(dto: dict):
    lesson = Lesson(**dto)
    await add_instance(lesson)
