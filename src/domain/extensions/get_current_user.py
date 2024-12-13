from fastapi import Depends
from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from src.infrastructure.redis import Users


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> Users:
    return Users.get(token)
