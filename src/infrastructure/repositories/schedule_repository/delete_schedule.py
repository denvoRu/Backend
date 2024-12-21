from src.infrastructure.database import (
    ScheduleLesson, delete_from_instance_by_id
)


async def delete_lesson(schedule_lesson_id: int):
    return await delete_from_instance_by_id(
        ScheduleLesson, 
        schedule_lesson_id
    )
