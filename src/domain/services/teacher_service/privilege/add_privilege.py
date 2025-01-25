from src.infrastructure.enums.privilege import Privilege
from src.infrastructure.repositories import teacher_repository
from src.infrastructure.exceptions import (
    TeacherNotFoundException,
    PrivilegeAlreadyExistsException,
)
                                        
from fastapi import Response, status
from uuid import UUID


async def add(teacher_id: UUID, privilege: Privilege):
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()

    if await teacher_repository.privilege.has_by_name(teacher_id, privilege.value):
        raise PrivilegeAlreadyExistsException()

    await teacher_repository.privilege.add(teacher_id, privilege.value)
    return Response(status_code=status.HTTP_201_CREATED)
