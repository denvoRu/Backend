from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import teacher_repository
from src.infrastructure.exceptions import TeacherNotFoundException
                                        
from fastapi import Response, status
from bcrypt import gensalt, hashpw
from uuid import UUID


async def edit(teacher_id: UUID, dto: EditUserDTO):
    if not await teacher_repository.has_by_id(teacher_id):
        raise TeacherNotFoundException()
    
    salt = gensalt()
    dto.password = hashpw(dto.password.encode(), salt).decode()
    dto_dict = dto.model_dump(exclude_none=True)

    await teacher_repository.update_by_id(teacher_id, dto_dict)
    return Response(status_code=status.HTTP_200_OK)