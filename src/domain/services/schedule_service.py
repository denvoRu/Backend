from src.infrastructure.repositories import (
    schedule_repository, teacher_repository
)
from src.application.dto.schedule import (
    AddLessonInScheduleDTO, EditLessonInScheduleDTO
)

from fastapi import HTTPException, status


async def get_schedule(teacher_id: int, week: int = 1): 
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_schedule(teacher_id):
        return []
    
    return await schedule_repository.get_by_week(teacher_id, week)


async def add_lesson(teacher_id: int, dto: AddLessonInScheduleDTO):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_schedule(teacher_id):
        schedule_repository.add_schedule(teacher_id)

    dto_dict = dto.model_dump(exclude_none=True)
    schedule_id = await schedule_repository.get_schedule(teacher_id)

    await schedule_repository.add_lesson(schedule_id, dto_dict)
    return { "status": "ok" }
    

async def delete_lesson(teacher_id: int, schedule_lesson_id: int):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_schedule(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )

    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    await schedule_repository.delete_lesson(schedule_lesson_id)
    return { "status": "ok" }


async def edit_lesson(
    teacher_id: int, 
    schedule_lesson_id: int, 
    dto: EditLessonInScheduleDTO
): 
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_schedule(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found"
        )
    
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    dto_dict = dto.model_dump(exclude_none=True)
    await schedule_repository.edit_lesson(schedule_lesson_id, dto_dict)
    return { "status": "ok" }


async def import_from_modeus(teacher_id: int): 
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_schedule(teacher_id):
        schedule_repository.add_schedule(teacher_id)
    
    return { "status": "ok" }


async def set_start_date(teacher_id: int, start_date: str): ...