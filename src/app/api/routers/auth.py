from random import randint
from typing import Any
from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException, Response, status, Request, Depends
from fastapi.security import OAuth2PasswordRequestForm
from bcrypt import checkpw

from src.app.api.extensions.token import create_token
from src.app.api.extensions.validate import validate_email, validate_password, validate_name

router = APIRouter()


@router.post("/register", description="Register a new user")
async def register(name: str, email: str, password: str) -> Any:
    valid_check = validate_name(name) and validate_email(email) and validate_password(password)
    if not valid_check:
        return Response(status_code=403)
    user = ... # поиск по email

    if user is not None and user.auth_key is None:
        return Response(status_code=403)
    elif user is not None:
        await ... # удаление юзера из базы данных

    user = await ... # добавление юзера в базу данных и копирование в переменную

    return user.auth_key


@router.post("/login", description="Authorizes the user")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if form_data.username == "admin" and form_data.password == "password":
        return create_token({
            "email": "test@test.ru",
            "role": form_data.username
        })
