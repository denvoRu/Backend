from src.infrastructure.config.config import ALGORITHM, JWT_SECRET_KEY
from src.infrastructure.redis import Users

from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user(access_token: Annotated[str, Depends(oauth2_scheme)]) -> Users:
    try:
        jwt.decode(access_token, JWT_SECRET_KEY, ALGORITHM)
        return Users.find(Users.access_token == access_token).first()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
