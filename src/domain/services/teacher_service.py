from src.infrastructure.enums.privilege import Privilege
from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import teacher_repository
                                             
from fastapi import HTTPException, Response, status
from uuid import UUID


async def get_all(
        page: int = 1,
        limit: int = 10,
        columns: str = None,
        sort: str = None,
        search: str = None,
        desc: int = 0,
        rating_start: int = -1,
        rating_end: int = -1,
        subject_ids: str = None
):
    if subject_ids is not None:
        subject_ids = subject_ids.split(",")
        
    try:
        return await teacher_repository.get_all(
            page, 
            limit, 
            columns, 
            sort, 
            search, 
            desc,
            rating_start, 
            rating_end, 
            subject_ids
        )
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


async def edit(teacher_id: UUID, dto: EditUserDTO):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    dto_dict = dto.model_dump(exclude_none=True)

    await teacher_repository.update_by_id(teacher_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)


async def delete(teacher_id: UUID):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    await teacher_repository.delete_by_id(teacher_id)
    return Response(status_code=status.HTTP_200_OK)


async def get_privileges(teacher_id: UUID):    
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    return await teacher_repository.privelege.get_by_id(teacher_id)


async def add_privilege(teacher_id: UUID, privilege: Privilege):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    if await teacher_repository.privelege.has_by_name(teacher_id, privilege.value):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, 
            detail="Privilege already exists"
        )

    await teacher_repository.privelege.add(teacher_id, privilege.value)
    return Response(status_code=status.HTTP_201_CREATED)


async def delete_privilege(teacher_id: UUID, privilege: Privilege):
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )

    if not await teacher_repository.privelege.has_by_name(teacher_id, privilege.value):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Privilege does not exist"
        )
    
    await teacher_repository.privelege.delete_by_name(teacher_id, privilege.value)
    return Response(status_code=status.HTTP_200_OK)

