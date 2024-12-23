from src.application.dto.subject import CreateSubjectDTO, EditSubjectDTO
from src.infrastructure.repositories import (
    subject_repository, module_repository
)

from fastapi import HTTPException, Response, status
from uuid import UUID


async def get_all(
    page, limit, columns, sort, search, desc, 
    rating_start, rating_end, teacher_ids,
    module_id
):
    if teacher_ids is not None:
        teacher_ids = list(map(int, teacher_ids.split(",")))

    if search is not None and search != "":
        search = "name*{0}".format(search)
        
    try:
        return await subject_repository.get_all(
            page, limit, columns, sort, search, desc, 
            rating_start, rating_end, teacher_ids, module_id
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )


async def get_by_id(subject_id: UUID):
    if not await subject_repository.has_by_id(subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    return await subject_repository.get_by_id(subject_id)
    

async def create(dto: CreateSubjectDTO):
    if await subject_repository.has_by_name(dto.name):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Subject already exists"
        )
    
    if not await module_repository.has_by_id(dto.module_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Module not found"
        )
 
    await subject_repository.add(dto.module_id, dto.name)
    return Response(status_code=status.HTTP_201_CREATED)


async def edit(subject_id: UUID, dto: EditSubjectDTO):
    try:
        return await subject_repository.update_by_id(subject_id, dto)
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )


async def delete(subject_id: UUID):
    if not await subject_repository.has_by_id(subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
   
    return await subject_repository.delete_by_id(subject_id)
