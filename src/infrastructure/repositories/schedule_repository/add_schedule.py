from src.infrastructure.database import db, add, Schedule, ScheduleLesson


async def add_schedule(teacher_id: int):
    schedule = Schedule(
        teacher_id=teacher_id
    )
    await add(schedule)


async def add_lesson(schedule_id: int, dto: dict):
    schedule_lesson = ScheduleLesson(
        schedule_id=schedule_id,
        **dto
    )
    await add(schedule_lesson)