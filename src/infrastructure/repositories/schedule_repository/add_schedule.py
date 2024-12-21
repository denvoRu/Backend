from src.infrastructure.database import (
    Schedule, ScheduleLesson, add_instance
)


async def add(teacher_id: int):
    schedule = Schedule(
        teacher_id=teacher_id
    )
    await add_instance(schedule)


async def add_lesson(schedule_id: int, dto: dict):
    schedule_lesson = ScheduleLesson(
        schedule_id=schedule_id,
        **dto
    )
    await add_instance(schedule_lesson)
