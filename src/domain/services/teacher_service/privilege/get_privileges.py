from src.infrastructure.repositories import teacher_repository
from src.infrastructure.exceptions import (
    TeacherNotFoundException,
)
                                        
from uuid import UUID


async def get_all(teacher_id: UUID):
    """
    Gets teacher's privileges (is teacher allowed to see some statistics)
    """
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    return await teacher_repository.privilege.get_by_id(teacher_id)
