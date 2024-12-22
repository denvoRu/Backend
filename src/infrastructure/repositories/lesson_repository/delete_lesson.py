from src.infrastructure.database import Lesson, delete_from_instance_by_id


async def delete_by_id(lesson_id: int):
    return await delete_from_instance_by_id(Lesson, lesson_id)
