from src.domain.helpers.schedule.last_monday import get_last_monday
from src.domain.helpers.schedule.import_from_modeus import import_from_modeus_by_id
from src.application.dto.lesson import AddLessonDTO
from src.infrastructure.repositories import (
    lesson_repository, 
    schedule_repository,
    study_group_repository,
    teacher_repository, 
    subject_repository
)
from src.infrastructure.exceptions import (
    SubjectNotFoundException,
    TeacherNotFoundException
)

from uuid import UUID
from fastapi import Response, status


async def add(teacher_id: UUID, dto: AddLessonDTO):
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    if not await subject_repository.has_by_id(dto.subject_id):
        raise SubjectNotFoundException()

    if not await study_group_repository.has_by_ids(dto.subject_id, teacher_id):
        raise TeacherNotFoundException()
    
    if not await schedule_repository.has_by_id(teacher_id):
        await schedule_repository.add(teacher_id, get_last_monday())
    
    study_group_id = await study_group_repository.get_by_ids(
        teacher_id, 
        dto.subject_id
    )

    dto = dto.model_dump(
        exclude_none=True, 
        exclude={"subject_id"}, 
    )
    dto["study_group_id"] = study_group_id
    return await lesson_repository.add(dto)


async def add_from_modeus_on_week(teacher_id: UUID):
    modeus_lessons = await import_from_modeus_by_id(
        teacher_id, 
        with_counter=True,
        week_count=1
    )

    await lesson_repository.add_many_from_modeus(
        teacher_id,
        modeus_lessons,
        get_last_monday()
    )
    return Response(status_code=status.HTTP_201_CREATED)
