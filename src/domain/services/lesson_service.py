from src.infrastructure.repositories import (
    lesson_repository, schedule_repository
)

from fastapi import HTTPException, Response, status
from uuid import UUID


async def get_all(teacher_id: UUID):
    if not await schedule_repository.has_by_id(teacher_id):
        return []
    
    return await lesson_repository.get_by_teacher_id(teacher_id)