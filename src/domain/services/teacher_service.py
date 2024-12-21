from src.infrastructure.enums.privileges import Privileges
from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import teacher_repository
                                             
from fastapi import HTTPException, Response, status


async def get_teachers(
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        search: str = None,
        desc: int = 0
):
    if search is not None and search != "":
        search = "first_name*{0},second_name*{0},third_name*{0}".format(
            search
        )
        
    try:
        return await teacher_repository.all(page, limit, columns, sort, search, desc)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )


async def get_by_id(teacher_id: str):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    return await teacher_repository.get_by_id(teacher_id)


async def edit_teacher(teacher_id: int, dto: EditUserDTO):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    dto_dict = dto.model_dump(exclude_none=True)

    await teacher_repository.update_by_id(teacher_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)


async def delete_teacher(teacher_id: int):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    await teacher_repository.delete_by_id(teacher_id)
    return Response(status_code=status.HTTP_200_OK)


async def get_privileges(teacher_id: int):    
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    return await teacher_repository.get_privileges(teacher_id)


async def add_privilege(teacher_id: int, privilege: Privileges):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    if await teacher_repository.has_privilege(teacher_id, privilege.value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Privilege already exists"
        )

    await teacher_repository.add_privilege(teacher_id, privilege.value)
    return Response(status_code=status.HTTP_201_CREATED)


async def delete_privilege(teacher_id: int, privilege: Privileges):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    if not await teacher_repository.has_privilege(teacher_id, privilege.value):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Privilege does not exist"
        )
    
    await teacher_repository.delete_privilege(teacher_id, privilege.value)
    return Response(status_code=status.HTTP_200_OK)

async def get_rating(teacher_id: int): ...
