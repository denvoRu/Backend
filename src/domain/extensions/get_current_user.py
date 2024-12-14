from src.infrastructure.redis import Users

from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> Users:
    return Users.find(Users.access_token == access_token).all()[0]
