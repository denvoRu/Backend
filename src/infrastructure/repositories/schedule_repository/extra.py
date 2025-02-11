from src.infrastructure.database import (
    Schedule, ScheduleLesson, has_instance, get_by_id
)

from uuid import UUID


async def is_teacher_of_lesson(teacher_id: UUID, schedule_lesson_id: UUID):
    """
    Checks that teacher is related to schedule
    """
    schedule_id = await get_by_id(
        Schedule, 
        teacher_id, 
        "id", 
        "teacher_id"
    )

    return await has_instance(
        ScheduleLesson, 
        (ScheduleLesson.schedule_id == schedule_id,
        ScheduleLesson.id == schedule_lesson_id)
    )
    