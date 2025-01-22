from src.domain.extensions.token import decode_user
from src.infrastructure.redis import Users
from src.infrastructure.exceptions import NotValidateCredentialsException

from typing_extensions import Annotated
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
        access_token: Annotated[str, Depends(oauth2_scheme)]
) -> Users:
    """
    Gets current user
    :param access_token: token that we decode to recognize the user
    :return: current user if token is valid
    """
    try:
        decode_user(access_token)
        return Users.find(Users.access_token == access_token).first()
    except Exception:
        raise NotValidateCredentialsException()
