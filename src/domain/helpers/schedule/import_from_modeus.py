from src.domain.extensions import selenium
from src.infrastructure.repositories import (
    module_repository, subject_repository,
    schedule_repository, teacher_repository
)

from aiomodeus import AioModeus


async def import_from_modeus_by_id(
    teacher_id: dict, 
    week_count: int
):
    schedule_id = await schedule_repository.get_by_id(teacher_id)
    teacher = await teacher_repository.get_by_id(teacher_id)

    FIO = " ".join([
        teacher["second_name"], 
        teacher["first_name"], 
        teacher["third_name"]
    ])
    institute_id = teacher["institute_id"]

    token = selenium.auth()
    aim = AioModeus(token)  
 
    if week_count == 1:
        schedule = await aim.get_schedule_for_week_by_teacher_name(FIO)
        schedules = [schedule]
    else: 
        schedules = await aim.get_schedule_for_two_week_by_teacher_name(FIO)


    for schedule in schedules:
        not_founded_modules = await module_repository.not_has_from_modeus(
            institute_id, 
            schedule.unique_modules
        )
        not_founded_subjects = await subject_repository.not_has_from_modeus(
            schedule.unique_subjects
        )

        await module_repository.add_from_list(
            institute_id, 
            [x.name for x in not_founded_modules]
        )
        await subject_repository.add_from_modeus(
            institute_id, 
            not_founded_subjects
        )

        await schedule_repository.delete_all_lessons(schedule_id)

        if len(schedule.schedule_lessons) > 0:
            await schedule_repository.add_lesson_from_modeus(
                teacher_id,
                schedule_id, 
                schedule.schedule_lessons.get_in_unique_time()
            )
