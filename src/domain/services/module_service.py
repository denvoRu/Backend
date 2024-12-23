from src.application.dto.module import CreateModuleDTO
from src.infrastructure.repositories import module_repository

from fastapi import HTTPException, Response, status
from uuid import UUID


async def get_all_with_subjects(
        page, 
        limit, 
        sort, 
        search, 
        desc, 
        rating_start, 
        rating_end, 
        institute_ids,
        teacher_ids
): 
    if institute_ids is not None:
        institute_ids = institute_ids.split(",")
        
    if teacher_ids is not None:
        teacher_ids = teacher_ids.split(",")
        
    try: 
        return await module_repository.get_all_with_subjects(
            page, 
            limit, 
            sort, 
            search, 
            desc, 
            rating_start, 
            rating_end, 
            institute_ids,
            teacher_ids
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )


async def get_all(page, limit, columns, sort, search, desc): 
    if search is not None and search != "":
        search = "name*{0}".format(search)
        
    try:
        return await module_repository.get_all(
            page, limit, columns, sort, search, desc
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )


async def get_by_id(module_id: UUID): 
    if not await module_repository.has_by_id(module_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Module not found"
        )
    
    return await module_repository.get_by_id(module_id)


async def create(dto: CreateModuleDTO): 
    has_name = await module_repository.has_by_name(dto.name)
    if has_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Module already exists"
        )
    
    await module_repository.add(dto.institute_id, dto.name)
    return Response(status_code=status.HTTP_201_CREATED)


async def delete(module_id: UUID):
    has_id = await module_repository.has_by_id(module_id)
    if not has_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Module not found"
        )
    
    await module_repository.delete_by_id(module_id)
    return Response(status_code=status.HTTP_200_OK)
