from random import randint
from typing import Any
from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException, Response, status, Request, Depends
from bcrypt import checkpw

from src.domain.models.extended_oauth_request_form import ExtendedOAuth2PasswordRequestForm
from src.application.dto import RegisterDTO
from src.domain.extensions.token import create_token
from src.domain.extensions.validate import validate_email, validate_password

router = APIRouter()


@router.post("/register", description="Register a new user")
async def register(dto: RegisterDTO) -> Any:
    valid_check = validate_email(dto.email) and validate_password(dto.password)
    if not valid_check:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    user = ... # поиск по email

    if user is not None and user.auth_key is None:
        return Response(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY)
    elif user is not None:
        await ... # удаление юзера из базы данных

    user = await ... # добавление юзера в базу данных и копирование в переменную

    return user.auth_key


@router.post("/login", description="Authorizes the user")
async def login(form_data: Annotated[ExtendedOAuth2PasswordRequestForm, Depends()]):
    if form_data.username == "admin" and form_data.password == "password":
        return create_token({
            "email": "test@test.ru",
            "role": form_data.role
        })
