from src.infrastructure.repositories import (
    study_group_repository, subject_repository,
    teacher_repository
)
from src.infrastructure.exceptions import (
    SubjectNotFoundException,
    SubjectsAreRequiredException,
    TeacherNotFoundException,
    TeacherAlreadyExistsInSubjectException,
    OneOrMoreSubjectsNotFoundException
)

from fastapi import Response, status
from typing import List
from uuid import UUID


async def delete_by_teacher(subject_id: UUID, teacher_id: UUID):
    if not await subject_repository.has_by_id(subject_id):
        raise SubjectNotFoundException()
    
    if not await study_group_repository.has_by_ids(subject_id, teacher_id):
        raise TeacherAlreadyExistsInSubjectException()
     
    await study_group_repository.delete_by_subject(
        subject_id, 
        teacher_id
    )
    return Response(status_code=status.HTTP_200_OK)
    

async def delete_many(teacher_id: UUID, subject_ids: List[UUID]):
    if len(subject_ids) == 0:
        raise SubjectsAreRequiredException()
    
    if not await subject_repository.has_many(subject_ids):
        raise OneOrMoreSubjectsNotFoundException()
    
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    for subject_id in subject_ids:
        if not await study_group_repository.has_by_ids(subject_id, teacher_id):
            raise TeacherNotFoundException()
    
    await study_group_repository.delete_many(teacher_id, subject_ids)
    return Response(status_code=status.HTTP_200_OK)
