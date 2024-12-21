from src.application.dto.subject import CreateSubjectDTO, EditSubjectDTO
from src.infrastructure.repositories import (
    subject_repository, institute_repository, module_repository
)
from fastapi import HTTPException, status


async def get_all(
    page, limit, columns, sort, search, desc, 
    rating_start, rating_end, teacher_ids,
    module_id
):
    if teacher_ids is not None:
        teacher_ids = teacher_ids.split(",")
    try:
        if search is not None and search != "":
            search = "name*{0}".format(search)
        return await subject_repository.get_all(
            page, limit, columns, sort, search, desc, 
            rating_start, rating_end, teacher_ids, module_id
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )

async def get_by_id(subject_id: int):
    try:
        return await subject_repository.get_by_id(subject_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )

async def create_subject(dto: CreateSubjectDTO):
    if await subject_repository.has_by_name(dto.name):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Subject already exists"
        )
    
    has_by_name = await institute_repository.has_by_id(dto.institute_id)
    if not has_by_name:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Institute not found"
        )
    
    has_module = await module_repository.has_by_id(dto.module_id)
    if not has_module:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Module not found"
        )
    
    try:
        await subject_repository.add(dto.institute_id, dto.module_id, dto.name)
        return { "status": "ok" }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )

async def edit_subject(subject_id: int, dto: EditSubjectDTO):
    try:
        return await subject_repository.update_by_id(subject_id, dto)
    except:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more parameters are invalid"
        )

async def delete_subject(subject_id: int):
    try:
        return await subject_repository.delete_by_id(subject_id)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    