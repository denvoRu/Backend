from src.infrastructure.repositories import (
    study_group_repository, subject_repository
)
from fastapi import HTTPException, status


async def show_teachers(
        subject_id, 
        page: int = 1, 
        limit: int = 10, 
        columns: str = None, 
        sort: str = None, 
        search: str = None, 
        desc: int = 0
):
    if not await subject_repository.has_by_id(subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    if search is not None and search != "":
        search = "first_name*{0},second_name*{0},third_name*{0},email*{0}".format(search)
    
    return await study_group_repository.get_by_id(
        subject_id, 
        page, 
        limit, 
        columns,
        sort, 
        search, 
        desc
    )

    
    
async def add_teacher(subject_id: int, teacher_id: int):
    if not await subject_repository.has_by_id(subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    if await study_group_repository.has_by_id(subject_id, teacher_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Teacher already exists in subject"
        )
    
    await study_group_repository.add(subject_id, teacher_id)
    return { "status": "ok" }
    
    
async def delete_teacher(subject_id: int, teacher_id: int):
    if not await subject_repository.has_by_id(subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    if not await study_group_repository.has_by_id(subject_id, teacher_id):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Teacher already exists in subject"
        )
     
    await study_group_repository.delete_from_subject(
        subject_id, teacher_id
    )
    return { "status": "ok" }
    