from src.domain.extensions.get_hex_uuid import get_hex_uuid
from src.infrastructure.enums.role import Role
from src.infrastructure.repositories.institute_repository import (
    has_by_id, update_password
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

from fastapi import HTTPException, status
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
    
    is_has = await has_by_id(dto.institute_id)
    if dto.role == Role.TEACHER and not(is_has):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Institute not found"
        )
    
    salt = gensalt()
    hashed_password = hashpw(dto.password.encode(), salt).decode()

    await add_in_teacher_or_admin(dto, hashed_password)
    # await EmailSender.send_registered(dto.email, dto.password)

    return { "status": "ok" }

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
    if await is_in_teacher_or_admin(dto.email, dto.role):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists"
        )
    
    restore_token = get_hex_uuid()
    add_restore_data_in_redis(dto.email, dto.role, restore_token)
    restore_password_link = get_restore_password_link(restore_token)
    await EmailSender.send_update_password(dto.email, restore_password_link)
    return { "status": "ok" }

async def update_password_from_token(dto: UpdatePasswordDTO):
    try:
        rp = get_restore_token_from_redis(dto.restore_token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Restore token is expired"
        ) 
    
    await update_password(rp.email, rp.role, dto.password) 
    return { "status": "ok" }