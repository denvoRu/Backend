from src.infrastructure.enums.privileges import Privileges
from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import (
    administrator_repository, teacher_repository
)
from fastapi import HTTPException, status


async def show_teachers(
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        filter: str = None,
        desc: int = 0
):
    return await teacher_repository.all(page, limit, columns, sort, filter, desc)

async def get_by_id(teacher_id: str):
    return await teacher_repository.get_by_id(teacher_id)

async def edit_teacher(admin_id: int, dto: EditUserDTO):
    await administrator_repository.edit_teacher(admin_id, dto)
    return { "status": "ok" }

async def delete_teacher(teacher_id: int):
    await teacher_repository.delete_teacher(teacher_id)
    return { "status": "ok" }

async def get_privileges(teacher_id: int):
    data = await teacher_repository.get_privileges(teacher_id)
    if len(data) > 0:
        return list([i[0] for i in data])
    return []

async def add_privilege(teacher_id: int, privilege: Privileges):
    hasPrivilege = await teacher_repository.has_privilege(teacher_id, privilege.value)
    if hasPrivilege:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Privilege already exists"
        )
    
    await teacher_repository.add_privilege(teacher_id, privilege.value)
    return { "status": "ok" }

async def delete_privilege(teacher_id: int, privilege: Privileges):
    hasPrivilege = await teacher_repository.has_privilege(teacher_id, privilege.value)
    
    if not hasPrivilege:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Privilege does not exist"
        )
    
    await teacher_repository.delete_privilege(teacher_id, privilege.value)
    return { "status": "ok" }