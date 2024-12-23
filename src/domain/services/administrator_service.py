from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import administrator_repository

from fastapi import HTTPException, Response, status
from uuid import UUID


async def get_all(page, limit, columns, sort, search, desc): 
    try:
        return await administrator_repository.get_all(
            page, limit, columns, sort, search, desc
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )


async def get_by_id(admin_id: str):
    if not await administrator_repository.has_by_id(admin_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrator not found"
        )
    
    return await administrator_repository.get_by_id(admin_id)


async def edit(admin_id: UUID, dto: EditUserDTO):
    if not await administrator_repository.has_by_id(admin_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrator not found"
        )

    dto_dict = dto.model_dump(exclude_none=True)

    await administrator_repository.update_by_id(admin_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)


async def delete(admin_id: str):
    if not await administrator_repository.has_by_id(admin_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrator not found"
        )
    
    await administrator_repository.delete_by_id(admin_id)
    return Response(status_code=status.HTTP_200_OK)
        