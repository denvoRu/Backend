from src.application.dto.module import CreateModuleDTO
from src.infrastructure.repositories import module_repository

from fastapi import HTTPException, status


async def get_by_id(module_id: int): 
    try:
        return await module_repository.get_by_id(module_id)
    except TypeError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )

async def get_all(page, limit, columns, sort, search, desc): 
    try: 
        return await module_repository.get_all(page, limit, columns, sort, search, desc)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )

async def create_module(dto: CreateModuleDTO): 
    has_name = await module_repository.has_by_name(dto.name)
    if has_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Module already exists"
        )
    
    await module_repository.add(dto.name)
    return { "status": "ok" }

async def delete(module_id: int):
    has_id = await module_repository.has_by_id(module_id)
    if not has_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Module not found"
        )
    
    await module_repository.delete_by_id(module_id)
    return { "status": "ok" }