from src.domain.services import auth_service
from src.domain.extensions.check_role import CurrentAdmin
from src.domain.models.extended_oauth_request_form import ExtendedOAuth2PasswordRequestForm
from src.application.dto import RegisterDTO

from typing import Any, Union
from typing_extensions import Annotated
from fastapi import APIRouter, Depends


router = APIRouter()


@router.post("/register", description="Register a new user")
async def register(dto: Union[CurrentAdmin, RegisterDTO]) -> Any:
    return auth_service.register(dto)

@router.post("/login", description="Authorizes the user")
async def login(form_data: Annotated[ExtendedOAuth2PasswordRequestForm, Depends()]):
    return auth_service.login(form_data)

@router.post("/token", description="Get new token, if old token is valid")
async def token(token: str):
    return auth_service.token(token)
