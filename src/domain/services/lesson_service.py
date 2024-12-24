from src.infrastructure.repositories import (
    lesson_repository, schedule_repository
)

from fastapi import HTTPException, Response, status
from datetime import date
from uuid import UUID


async def get_all(teacher_id: UUID, start_date: date, end_date: date):
    if not await schedule_repository.has_by_id(teacher_id):
        return []
    
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Start date must be before end date"
        )
    
    if (end_date.day - start_date.day) > 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Interval must be less than 7 days"
        )
    
    lessons = await lesson_repository.get_all(teacher_id, start_date, end_date)

    future_lessons = await schedule_repository.get_in_interval(
        teacher_id,
        start_date, 
        end_date
    )
    
    lessons.extend(future_lessons)

    return lessons