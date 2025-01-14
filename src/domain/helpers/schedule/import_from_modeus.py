from src.domain.extensions import selenium
from src.infrastructure.repositories import (
    schedule_repository, teacher_repository
)

from uuid import UUID
from aiomodeus import AioModeus


async def import_from_modeus_by_id(
    teacher_id: UUID, 
    subject_id: UUID,
    week_count: int
):
            
    schedule_id = await schedule_repository.get_by_id(teacher_id)
    teacher = await teacher_repository.get_by_id(teacher_id)

    FIO = " ".join([
        teacher["second_name"], 
        teacher["first_name"], 
        teacher["third_name"]
    ])

    token = selenium.auth()
    aim = AioModeus(token)  
 
    if week_count == 1:
        schedule = await aim.get_schedule_for_week_by_teacher_name(FIO)
        schedules = (schedule, )
    else: 
        schedules = await aim.get_schedule_for_two_week_by_teacher_name(FIO)

    for schedule in schedules:
        schedule_lessons = await schedule_repository.get_exists_by_subject_id(
            schedule,
            subject_id
        )
        await schedule_repository.delete_all_lessons(schedule_id)
        
        if len(schedule_lessons) > 0:
            await schedule_repository.add_lesson_from_modeus(
                schedule_id, 
                schedule_lessons.get_in_unique_time()
            )
