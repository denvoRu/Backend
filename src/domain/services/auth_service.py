from domain.extensions.email.email_sender import EmailSender

from src.domain.extensions.token import create_token
from src.application.dto.auth.register_dto import RegisterDTO

from src.domain.helpers.auth import (
    add_in_teacher_or_admin, get_user_password_by_email_and_role, 
    is_in_teacher_or_admin, add_token_in_redis
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
        add_token_in_redis(form_data.username, form_data.role, token)
        return token

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, 
        detail="Incorrect username or password"
    )

    
