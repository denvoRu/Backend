from src.infrastructure.database import (
    Schedule, ScheduleLesson, has_instance
)


async def has_by_id(teacher_id: int):
    return await has_instance(
        Schedule, 
        Schedule.teacher_id == teacher_id
    )


async def has_lesson(schedule_lesson_id: int):
    return await has_instance(
        ScheduleLesson, 
        ScheduleLesson.id == schedule_lesson_id
    )
