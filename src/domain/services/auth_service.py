from src.domain.extensions.get_hex_uuid import get_hex_uuid
from src.infrastructure.enums.role import Role
from src.infrastructure.repositories import (
    institute_repository, study_group_repository, subject_repository,
    auth_repository
)
from src.domain.extensions.email.email_sender import EmailSender
from src.domain.extensions.token import create_token
from src.application.dto.auth import (
    RegisterDTO, RestorePasswordDTO, UpdatePasswordDTO
)
from src.domain.helpers.auth import (
    add_in_teacher_or_admin, get_user_password_and_id_by_email_and_role, 
    is_in_teacher_or_admin, add_token_in_redis, is_token_in_redis,
    create_new_user_by_token, add_restore_data_in_redis,
    get_restore_password_link, get_restore_token_from_redis
)

from fastapi import HTTPException, Response, status
from bcrypt import checkpw, hashpw, gensalt
from fastapi.security import OAuth2PasswordRequestForm


async def register(dto: RegisterDTO) -> str:
    if await is_in_teacher_or_admin(dto.email, dto.role):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists"
        )
    
    if dto.role == Role.TEACHER and not dto.institute_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Institute id is required"
        )
    
    has_subjects = len(dto.subjects) > 0 and dto.role == Role.TEACHER

    if has_subjects and not await subject_repository.has_many(dto.subjects):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="One or more subjects not found"
            )
    
    is_has = await institute_repository.has_by_id(dto.institute_id)
    if dto.role == Role.TEACHER and not(is_has):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Institute not found"
        )
    
    salt = gensalt()
    hashed_password = hashpw(dto.password.encode(), salt).decode()

    user = await add_in_teacher_or_admin(dto, hashed_password)
    # await EmailSender.send_registered(dto.email, dto.password)
    if has_subjects:
        await study_group_repository.add_many(user.id, dto.subjects)
    return Response(status_code=status.HTTP_201_CREATED)


async def login(form_data: OAuth2PasswordRequestForm, role: Role) -> str:
    user = await get_user_password_and_id_by_email_and_role(
        form_data.username, role
    )

    if checkpw(form_data.password.encode(), user.password.encode()):
        token = create_token(user.id, role)
        pk = add_token_in_redis(
            user.id, role, 
            token.access_token, token.refresh_token
        )
        if pk != token.refresh_token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error adding token in redis"
            )
        
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Incorrect username or password"
    )


async def token(refresh_token: str) -> str:
    if not is_token_in_redis(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid refresh_token"
        )
    
    token = create_new_user_by_token(refresh_token)
    return token

    
async def restore_password(dto: RestorePasswordDTO):
    if not await is_in_teacher_or_admin(dto.email, dto.role):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User not found"
        )
    
    restore_token = get_hex_uuid()
    add_restore_data_in_redis(dto.email, dto.role, restore_token)
    restore_password_link = get_restore_password_link(restore_token)
    # await EmailSender.send_update_password(dto.email, restore_password_link)
    return Response(status_code=status.HTTP_200_OK)


async def update_password_from_token(dto: UpdatePasswordDTO):
    try:
        rp = get_restore_token_from_redis(dto.restore_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Restore token is expired"
        ) 
    
    await auth_repository.update_password(rp.email, rp.role, dto.password) 
    return Response(status_code=status.HTTP_200_OK)
