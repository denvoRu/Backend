from typing import Any
from typing_extensions import Annotated
from fastapi import APIRouter, HTTPException, Response, status, Request, Depends


from domain.services import auth_service
from src.domain.models.extended_oauth_request_form import ExtendedOAuth2PasswordRequestForm
from src.application.dto import RegisterDTO
from src.domain.extensions.token import create_token

router = APIRouter()


@router.post("/register", description="Register a new user")
async def register(dto: RegisterDTO) -> Any:
    return auth_service.register(dto)

@router.post("/login", description="Authorizes the user")
async def login(form_data: Annotated[ExtendedOAuth2PasswordRequestForm, Depends()]):
    return auth_service.login(form_data)
