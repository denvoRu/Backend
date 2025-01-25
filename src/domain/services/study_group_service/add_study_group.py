from src.infrastructure.repositories import (
    study_group_repository, 
    subject_repository,
    teacher_repository
)
from src.infrastructure.exceptions import (
    SubjectNotFoundException,
    TeacherNotFoundException,
    TeacherAlreadyExistsInSubjectException,
    OneOrMoreTeachersNotFoundException,
    OneOrMoreSubjectsNotFoundException
)

from fastapi import Response, status
from typing import List
from uuid import UUID


async def add_by_teacher_ids(subject_id: UUID, teacher_ids: List[UUID]):
    """
    Add teachers to study group
    """
    if not await subject_repository.has_by_id(subject_id):
        raise SubjectNotFoundException()
    
    if not await teacher_repository.has_many(teacher_ids):
        raise OneOrMoreTeachersNotFoundException()
    
    for teacher_id in teacher_ids:
        if await study_group_repository.has_by_ids(subject_id, teacher_id):
            raise TeacherAlreadyExistsInSubjectException()
    
    await study_group_repository.add_many_teachers(subject_id, teacher_ids)
    return Response(status_code=status.HTTP_201_CREATED)


async def add_by_subject_ids(teacher_id: UUID, subject_ids: List[UUID]):
    """
    Add subjects to study group
    """
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    if not await subject_repository.has_many(subject_ids):
        raise OneOrMoreSubjectsNotFoundException()
    
    for subject_id in subject_ids:
        if await study_group_repository.has_by_ids(subject_id, teacher_id):
            raise TeacherAlreadyExistsInSubjectException()
        
    await study_group_repository.add_many(teacher_id, subject_ids)
    return Response(status_code=status.HTTP_201_CREATED)
    

async def add_by_teacher_id(subject_id: UUID, teacher_id: UUID):
    """
    Add a study group by teacher and subject ids
    """
    if not await subject_repository.has_by_id(subject_id):
        raise SubjectNotFoundException()
    
    if await study_group_repository.has_by_ids(subject_id, teacher_id):
        raise TeacherAlreadyExistsInSubjectException()
    
    await study_group_repository.add(subject_id, teacher_id)
    return Response(status_code=status.HTTP_201_CREATED)
