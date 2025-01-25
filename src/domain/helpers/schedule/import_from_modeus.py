from src.domain.extensions import selenium
from src.infrastructure.repositories import (
    schedule_repository, 
    teacher_repository,
    subject_repository
)

from uuid import UUID
from aiomodeus import AioModeus


async def import_from_modeus_by_id(
    teacher_id: UUID, 
    subject_id: UUID,
    with_counter: bool = False
):
    teacher = await teacher_repository.get_by_id(teacher_id)
    subject = await subject_repository.get_by_id(subject_id)

    FIO = " ".join([
        teacher["second_name"], 
        teacher["first_name"], 
        teacher["third_name"]
    ])

    token = selenium.auth()
    aim = AioModeus(token)  
 
    schedules = await aim.get_schedule_for_two_week_by_teacher_name(
        FIO,
        subject_name=subject.name,
        with_counter=with_counter
    )

    return [
        await schedule_repository.get_exists_by_subject_id(
            schedule,
            subject_id
        ) for schedule in schedules
    ]
    
