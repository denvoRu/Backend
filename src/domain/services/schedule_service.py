from src.infrastructure.enums.week import Week
from src.infrastructure.enums.role import Role
from src.domain.extensions.check_role.user import User
from src.domain.helpers.schedule import get_last_monday
from src.infrastructure.repositories import (
    schedule_repository, teacher_repository
)
from src.application.dto.schedule import (
    AddLessonInScheduleDTO, EditLessonInScheduleDTO
)

from fastapi import HTTPException, Response, status
from uuid import UUID


async def get_by_teacher_id(teacher_id: UUID, week: Week = Week.FIRST): 
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_by_id(teacher_id):
        return []
    
    return await schedule_repository.get_by_week(teacher_id, week)


async def add_lesson(teacher_id: UUID, dto: AddLessonInScheduleDTO):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_by_id(teacher_id):
        week = get_last_monday()
        await schedule_repository.add(teacher_id, week)

    dto_dict = dto.model_dump(exclude_none=True)
    schedule_id = await schedule_repository.get_by_id(teacher_id)

    await schedule_repository.add_lesson(schedule_id, dto_dict)
    return Response(status_code=status.HTTP_201_CREATED)
    

async def delete_lesson(user: User, schedule_lesson_id: UUID):
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    check_teacher = schedule_repository.is_teacher_of_lesson(
        user.user_id, schedule_lesson_id
    )
    
    if user.role == Role.TEACHER and not await check_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    await schedule_repository.delete_lesson(schedule_lesson_id)
    return Response(status_code=status.HTTP_200_OK)


async def edit_lesson(
    user: User,
    schedule_lesson_id: UUID, 
    dto: EditLessonInScheduleDTO
):  
    if not await schedule_repository.has_lesson(schedule_lesson_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    
    check_teacher = schedule_repository.is_teacher_of_lesson(
        user.user_id, schedule_lesson_id
    )
    
    if user.role == Role.TEACHER and not await check_teacher:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )

    dto_dict = dto.model_dump(exclude_none=True)
    await schedule_repository.update_lesson_by_id(schedule_lesson_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)


async def import_from_modeus(teacher_id: UUID): 
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await schedule_repository.has_by_id(teacher_id):
        schedule_repository.add(teacher_id)

    # MODEUS API
    return Response(status_code=status.HTTP_200_OK)
