from src.domain.extensions.get_hex_uuid import get_hex_uuid
from src.infrastructure.enums.role import Role
from src.domain.models.user import User
from src.infrastructure.config.config import JWT_SECRET_KEY, ALGORITHM
from src.domain.models.token import Token

from jose import jwt
from typing import Union
from datetime import datetime, timedelta, timezone


def encode_user(data: dict, expires_delta: Union[timedelta, None] = None):
    """
    Takes a user and creates a JWT-data for it
    :param data: the data to be encoded
    :param expires_delta: the timedelta to expire the token
    :return: the JWT data
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=48)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_user(token):
    """
    Takes a JWT token and decodes the user
    """
    decoded_data = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=ALGORITHM)
    return decoded_data


def create_token(user_id: str, role: Role) -> Token:
    """
    Creates a JWT token with the given role and user id
    :param user_id: the user id
    :param role: the role of the user
    :return: the JWT token
    """
    access_token_expires = timedelta(hours=8)
    access_token = encode_user(
        data={"sub": str(user_id), "role": role}, 
        expires_delta=access_token_expires
    )
    
    return Token(
        access_token=access_token, 
        refresh_token=get_hex_uuid(), 
        token_type="bearer"
    )