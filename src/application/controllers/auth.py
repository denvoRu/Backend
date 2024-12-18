from src.infrastructure.enums.role import Role
from src.domain.services import auth_service
from src.domain.extensions.check_role import CurrentAdmin
from src.application.dto import RegisterDTO

from typing import Any
from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/register", description="Register a new user")
async def register(dto: RegisterDTO = Body(...)) -> Any:
    return await auth_service.register(dto)

@router.post("/login", description="Authorizes the user")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], 
    role: Role = Body(...)
):
    return await auth_service.login(form_data, role)

@router.post("/token", description="Get new token, if refresh token is valid")
async def token(refresh_token: str):
    return await auth_service.token(refresh_token)
