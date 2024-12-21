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
        search: str = None,
        desc: int = 0
):
    try:
        if search is not None and search != "":
            search = "first_name*{0},second_name*{0},third_name*{0},email*{0}".format(search)
        return await teacher_repository.all(page, limit, columns, sort, search, desc)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )

async def get_by_id(teacher_id: str):
    try:
        return await teacher_repository.get_by_id(teacher_id)
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

async def edit_teacher(admin_id: int, dto: EditUserDTO):
    try:
        await administrator_repository.edit_teacher(admin_id, dto)
        return { "status": "ok" }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

async def delete_teacher(teacher_id: int):
    try:
        await teacher_repository.delete_teacher(teacher_id)
        return { "status": "ok" }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

async def get_privileges(teacher_id: int):
    try:
        data = await teacher_repository.get_privileges(teacher_id)
        if len(data) > 0:
            return list([i[0] for i in data])
        return []
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

async def add_privilege(teacher_id: int, privilege: Privileges):
    hasPrivilege = await teacher_repository.has_privilege(teacher_id, privilege.value)
    if hasPrivilege:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Privilege already exists"
        )
    
    try: 
        await teacher_repository.add_privilege(teacher_id, privilege.value)
        return { "status": "ok" }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

async def delete_privilege(teacher_id: int, privilege: Privileges):
    hasPrivilege = await teacher_repository.has_privilege(teacher_id, privilege.value)
    
    if not hasPrivilege:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Privilege does not exist"
        )
    
    try:
        await teacher_repository.delete_privilege(teacher_id, privilege.value)
        return { "status": "ok" }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

async def get_rating(teacher_id: int):
    return 