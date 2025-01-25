from src.infrastructure.enums.role import Role
from src.domain.extensions.email.email_sender import EmailSender
from src.application.dto.auth import RegisterDTO
from src.infrastructure.repositories import (
    institute_repository, 
    study_group_repository, 
    subject_repository,
)
from src.infrastructure.exceptions import (
    InstituteNotFoundException, 
    InstituteIsRequiredException,
    SubjectNotFoundException,
    UserAlreadyExistsException,
)
from src.domain.helpers.auth import (
    add_in_teacher_or_admin, 
    is_in_teacher_or_admin
)

from fastapi import Response, status
from bcrypt import hashpw, gensalt


async def register(dto: RegisterDTO) -> str:
    # some checks if something's wrong with current register try
    if await is_in_teacher_or_admin(dto.email, dto.role):
        raise UserAlreadyExistsException()
    
    if dto.role == Role.TEACHER and not dto.institute_id:
        raise InstituteIsRequiredException()
    
    has_subjects = len(dto.subjects) > 0 and dto.role == Role.TEACHER

    if has_subjects and not await subject_repository.has_many(dto.subjects):
            raise SubjectNotFoundException()
    
    is_has = await institute_repository.has_by_id(dto.institute_id)
    if dto.role == Role.TEACHER and not(is_has):
        raise InstituteNotFoundException()

    # creating hashed password, user and his subjects if needed
    salt = gensalt()
    hashed_password = hashpw(dto.password.encode(), salt).decode()

    user = await add_in_teacher_or_admin(dto, hashed_password)
    # await EmailSender.send_registered(dto.email, dto.password)
    if has_subjects:
        await study_group_repository.add_many(user.id, dto.subjects)
        
    return Response(status_code=status.HTTP_201_CREATED)
