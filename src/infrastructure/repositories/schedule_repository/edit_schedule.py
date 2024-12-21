from src.infrastructure.database import update, ScheduleLesson


async def edit_lesson(schedule_lesson_id: int, dto: dict):
    return await update.update_instance(
        ScheduleLesson,
        schedule_lesson_id,
        dto
    )