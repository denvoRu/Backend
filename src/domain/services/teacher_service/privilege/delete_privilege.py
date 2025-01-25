from src.infrastructure.repositories import subject_repository
from src.infrastructure.enums.privilege import Privilege
from src.infrastructure.repositories import teacher_repository
from src.infrastructure.exceptions import (
    TeacherNotFoundException,
    PrivilegeNotFoundException
)
                                        
from fastapi import Response, status
from uuid import UUID


async def delete(teacher_id: UUID, privilege: Privilege):
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()

    if not await teacher_repository.privilege.has_by_name(teacher_id, privilege.value):
        raise PrivilegeNotFoundException()
    
    await teacher_repository.privilege.delete_by_name(teacher_id, privilege.value)
    return Response(status_code=status.HTTP_200_OK)
