from src.infrastructure.repositories import teacher_repository
from src.infrastructure.exceptions import (
    TeacherNotFoundException,
)
                                        
from fastapi import Response, status
from uuid import UUID


async def delete(teacher_id: UUID):
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    await teacher_repository.delete_by_id(teacher_id)
    return Response(status_code=status.HTTP_200_OK)