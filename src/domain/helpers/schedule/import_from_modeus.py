from src.domain.extensions import selenium
from src.infrastructure.repositories import (
    schedule_repository, 
    teacher_repository,
    subject_repository
)

from uuid import UUID
from aiomodeus import AioModeus
from datetime import datetime


async def import_from_modeus_by_id(
    teacher_id: UUID, 
    *,
    subject_id: UUID = None,
    with_counter: bool = False,
    week_count: int = 2
):
    teacher = await teacher_repository.get_by_id(teacher_id)
    if subject_id:
        subject = await subject_repository.get_by_id(subject_id)
        subject_name = subject.name
    else:
        subject_name = None

    FIO = " ".join([
        teacher["second_name"], 
        teacher["first_name"], 
        teacher["third_name"]
    ])

    token = selenium.auth()
    aim = AioModeus(token)  
    
    if week_count == 1:
        schedules = await aim.get_schedule_for_week_by_teacher_name(
            FIO,
            subject_name=subject_name,
            with_counter=with_counter,
            custom_date=datetime(2025, 2, 25)
        )

        result = await schedule_repository.get_exists_by_subject_id(
            schedules, 
            subject_id
        )
    else:
        schedules = await aim.get_schedule_for_two_week_by_teacher_name(
            FIO,
            subject_name=subject_name,
            with_counter=with_counter,
            custom_date=datetime(2025, 2, 25)
        )

        result = await schedule_repository.get_exists_by_subject_id(
            schedules[0], 
            subject_id
        )

        result.extend(
            await schedule_repository.get_exists_by_subject_id(
                schedules[1], 
                subject_id
            )
        )
    
    return result
    
    
