from src.infrastructure.enums.role import Role
from src.domain.extensions.email.email_sender import EmailSender
from src.domain.extensions.token import create_token
from src.application.dto.auth.register_dto import RegisterDTO

from src.domain.helpers.auth import (
    add_in_teacher_or_admin, get_user_password_by_email_and_role, 
    is_in_teacher_or_admin, add_token_in_redis, is_token_in_redis,
    create_new_user_by_token
)

from fastapi import HTTPException, status
from bcrypt import checkpw, hashpw, gensalt
from fastapi.security import OAuth2PasswordRequestForm

async def register(dto: RegisterDTO) -> str:
    if await is_in_teacher_or_admin(dto.username, dto.role):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists"
        )
    
    salt = gensalt()
    hashed_password = hashpw(dto.password.encode(), salt).decode()

    print(await add_in_teacher_or_admin(dto, hashed_password))
    EmailSender.send_registered(dto.username, dto.password)

    return { "status": "ok" }

async def login(form_data: OAuth2PasswordRequestForm, role: Role) -> str:
    password = await get_user_password_by_email_and_role(
        form_data.username, role
    )

    if checkpw(form_data.password.encode(), password.encode()):
        token = create_token(form_data, role)
        pk = add_token_in_redis(
            form_data.username, role, 
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
    # Выдаёт ошибку
    print(is_token_in_redis(refresh_token))
    if not is_token_in_redis(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid refresh_token"
        )
    
    token = create_new_user_by_token(refresh_token)
    return token

    
