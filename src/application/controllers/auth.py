from src.infrastructure.enums.role import Role
from src.domain.services import auth_service
from src.domain.extensions.check_role import CurrentAdmin
from src.application.dto.auth import (
    RegisterDTO, 
    RestorePasswordDTO, 
    UpdatePasswordDTO
)

from typing import Any
from typing_extensions import Annotated
from fastapi import APIRouter, Body, Depends
from fastapi.security import OAuth2PasswordRequestForm


router = APIRouter()


@router.post("/register", description="Register a new user (for admins)", status_code=201)
async def register(
    admin: CurrentAdmin, 
    dto: RegisterDTO = Body(...)
) -> Any:
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


@router.post("/restore_password", description="Restore password for user")
async def restore_password(dto: RestorePasswordDTO = Body(...)):
    return await auth_service.restore_password(dto)


@router.post("/update_password", description="Update password for user")
async def update_password(dto: UpdatePasswordDTO = Body(...)):
    return await auth_service.update_password_from_token(dto)
