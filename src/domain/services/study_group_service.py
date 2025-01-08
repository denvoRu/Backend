from src.infrastructure.repositories import (
    study_group_repository, subject_repository,
    teacher_repository, lesson_repository
)

from fastapi import HTTPException, Response, status
from typing import List
from uuid import UUID


async def get_teachers(
        subject_id, 
        page: int = 1, 
        limit: int = 10, 
        columns: str = None, 
        sort: str = None, 
        search: str = None, 
        desc: int = 0
):
    """
    Get all teachers from study group
    :param subject_id: id of subject
    :param page: page number
    :param limit: count of teachers to show
    :param columns: fields to show
    :param sort: sort order
    :param search: search string
    :param desc: descending order
    """
    if not await subject_repository.has_by_id(subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    if search is not None and search != "":
        search = "first_name*{0},second_name*{0},third_name*{0}".format(search)
    
    return await teacher_repository.get_by_study_group(
        subject_id, 
        page, 
        limit, 
        columns,
        sort, 
        search, 
        desc
    )

async def add_by_teacher_ids(subject_id: UUID, teacher_ids: List[UUID]):
    """
    Add teachers to study group
    """
    if not await subject_repository.has_by_id(subject_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found"
        )
    
    if not await teacher_repository.has_many(teacher_ids):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more teachers not found"
        )
    
    for teacher_id in teacher_ids:
        if await study_group_repository.has_by_id(subject_id, teacher_id):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Teacher already exists in subject"
            )
    
    await study_group_repository.add_many_teachers(subject_id, teacher_ids)
    return Response(status_code=status.HTTP_201_CREATED)


async def add_by_subject_ids(teacher_id: UUID, subject_ids: List[UUID]):
    """
    Add subjects to study group
    """
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    if not await subject_repository.has_many(subject_ids):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="One or more subjects not found"
        )
    
    for subject_id in subject_ids:
        if await study_group_repository.has_by_id(subject_id, teacher_id):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Teacher already exists in subject"
            )
        
    await study_group_repository.add_many(teacher_id, subject_ids)
    return Response(status_code=status.HTTP_201_CREATED)
    

async def add_by_teacher_id(subject_id: UUID, teacher_id: UUID):
    """
    Add a study group by teacher and subject ids
    """
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
    return Response(status_code=status.HTTP_201_CREATED)
    
    
async def delete_teacher(subject_id: UUID, teacher_id: UUID):
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
    return Response(status_code=status.HTTP_200_OK)
    

async def delete_many(teacher_id: UUID, subject_ids: List[UUID]):
    if len(subject_ids) == 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Subject ids are required"
        )
    
    if not await subject_repository.has_many(subject_ids):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="One or more subjects not found"
        )
    
    if not await teacher_repository.has_by_id(teacher_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Teacher not found"
        )
    
    for subject_id in subject_ids:
        if not await study_group_repository.has_by_id(subject_id, teacher_id):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Teacher not found in subject"
            )
    
    await study_group_repository.delete_many(teacher_id, subject_ids)
    return Response(status_code=status.HTTP_200_OK)


async def get_active(study_group_id: UUID):
    try:
        return await lesson_repository.get_active_by_study_group_id(study_group_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Lesson not found"
        )
    