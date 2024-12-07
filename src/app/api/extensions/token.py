from datetime import datetime, timedelta, timezone
from src.app.config.config import JWT_SECRET_KEY, ALGORITHM
from src.app.api.models.token import Token
from jose import jwt

from typing import Union


def encode_user(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(hours=48)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=JWT_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_user(token):
    decoded_data = jwt.decode(token, key=JWT_SECRET_KEY, algorithms=ALGORITHM)
    return decoded_data


def create_token(user) -> Token:
    access_token_expires = timedelta(minutes=3600)
    access_token = encode_user(
        data={"sub": user["email"], "role": user["role"]}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")