from fastapi import HTTPException, status
from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import administrator_repository


async def get_by_id(admin_id: str):
    try:
        return await administrator_repository.get_by_id(admin_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrator not found"
        )

async def show_administrators(page, limit, columns, sort, search, desc): 
    try:
        return await administrator_repository.all(
            page, limit, columns, sort, search, desc
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )

async def edit_administrator(admin_id: int, dto: EditUserDTO):
    try:
        await administrator_repository.edit_admin(admin_id, dto)
        return { "status": "ok" }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrator not found"
        )

async def delete_administrator(admin_id: str):
    try:
        await administrator_repository.delete_admin(admin_id)
        return { "status": "ok" }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Administrator not found"
        )