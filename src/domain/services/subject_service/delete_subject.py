from src.infrastructure.repositories import subject_repository
from src.infrastructure.exceptions import SubjectNotFoundException

from uuid import UUID


async def delete(subject_id: UUID):
    if not await subject_repository.has_by_id(subject_id):
        raise SubjectNotFoundException()
   
    return await subject_repository.delete_by_id(subject_id)
