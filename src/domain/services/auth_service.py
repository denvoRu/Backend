from src.infrastructure.enums.role import Role
from src.infrastructure.repositories. institute_repository import has_institute_by_id
from src.domain.extensions.email.email_sender import EmailSender
from src.domain.extensions.token import create_token
from src.application.dto.auth.register_dto import RegisterDTO

from src.domain.helpers.auth import (
    add_in_teacher_or_admin, get_user_password_and_id_by_email_and_role, 
    is_in_teacher_or_admin, add_token_in_redis, is_token_in_redis,
    create_new_user_by_token
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
    
    if dto.role == Role.ADMINISTRATOR and dto.institute_id:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Institute id is not required"
        )
    
    is_has = await has_institute_by_id(dto.institute_id)
    if dto.role == Role.TEACHER and not(is_has):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Institute not found"
        )
    
    salt = gensalt()
    hashed_password = hashpw(dto.password.encode(), salt).decode()

    await add_in_teacher_or_admin(dto, hashed_password)
    EmailSender.send_registered(dto.email, dto.password)

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

    
