from src.domain.extensions.email.email_sender import EmailSender
from src.domain.extensions.token import create_token
from src.application.dto.auth.register_dto import RegisterDTO

from src.domain.helpers.auth import (
    add_in_teacher_or_admin, get_user_password_by_email_and_role, 
    is_in_teacher_or_admin, add_token_in_redis, is_token_in_redis,
    create_new_user_by_token
)
from src.domain.models.extended_oauth_request_form import (
    ExtendedOAuth2PasswordRequestForm
)

from fastapi import HTTPException, status
from bcrypt import checkpw, hashpw, gensalt

def register(dto: RegisterDTO) -> str:
    if is_in_teacher_or_admin(dto.username, dto.role):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="User already exists"
        )
    
    salt = gensalt()
    hashed_password = hashpw(dto.password.encode(), salt).decode()

    add_in_teacher_or_admin(dto, hashed_password)
    EmailSender.send_registered(dto.username, dto.password)

    return { "status": "ok" }

def login(form_data: ExtendedOAuth2PasswordRequestForm) -> str:
    password = get_user_password_by_email_and_role(
        form_data.username, form_data.role
    )
    
    if checkpw(form_data.password, password):
        token = create_token(form_data)
        pk = add_token_in_redis(form_data.username, form_data.role, token.access_token)

        if pk != token.access_token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Error adding token in redis"
            )
        
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Incorrect username or password"
    )

def token(token: str) -> str:
    if not is_token_in_redis(token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid token"
        )
    
    token = create_new_user_by_token(token)
    return token
    
