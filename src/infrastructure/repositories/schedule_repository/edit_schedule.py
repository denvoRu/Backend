from src.infrastructure.database import ScheduleLesson, update_instance


async def update_lesson_by_id(schedule_lesson_id: int, dto: dict):
    return await update_instance(
        ScheduleLesson,
        schedule_lesson_id,
        dto
    )