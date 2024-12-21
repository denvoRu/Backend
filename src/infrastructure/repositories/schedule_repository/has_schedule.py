from src.infrastructure.database import Schedule, ScheduleLesson, has

async def has_schedule(teacher_id: int):
    return await has.has_instance(
        Schedule, 
        Schedule.teacher_id == teacher_id
    )

async def has_lesson(schedule_lesson_id: int):
    return await has.has_instance(
        ScheduleLesson, 
        ScheduleLesson.id == schedule_lesson_id
    )