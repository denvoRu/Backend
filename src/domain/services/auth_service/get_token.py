from src.infrastructure.exceptions import IncorrectUsernameOrPasswordException
from src.infrastructure.enums.role import Role
from src.domain.extensions.email.email_sender import EmailSender
from src.domain.extensions.token import create_token
from src.domain.helpers.auth import (
    get_user_password_and_id_by_email_and_role, 
    add_token_in_redis,
    is_token_in_redis,
    create_new_user_by_token
)

from fastapi import HTTPException, status
from bcrypt import checkpw
from fastapi.security import OAuth2PasswordRequestForm


async def login(form_data: OAuth2PasswordRequestForm, role: Role) -> str:
    try:
        user = await get_user_password_and_id_by_email_and_role(
            form_data.username, role
        )
    except Exception:
        raise IncorrectUsernameOrPasswordException

    if checkpw(form_data.password.encode(), user.password.encode()):
        token = create_token(user.id, role)
        pk = add_token_in_redis(
            user.id, role, 
            token.access_token, token.refresh_token
        )
        if pk != token.refresh_token:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return token

    raise IncorrectUsernameOrPasswordException


async def token(refresh_token: str) -> str:
    if not is_token_in_redis(refresh_token):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid refresh_token"
        )

    # creates new token for user
    token = create_new_user_by_token(refresh_token)
    return token
