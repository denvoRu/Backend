from src.application.dto.subject import EditSubjectDTO
from src.infrastructure.exceptions import InvalidParametersException
from src.infrastructure.repositories import subject_repository

from uuid import UUID
    

async def edit(subject_id: UUID, dto: EditSubjectDTO):
    try:
        dto = dto.model_dump(exclude_none=True)
        return await subject_repository.update_by_id(subject_id, dto)
    except:
        raise InvalidParametersException()