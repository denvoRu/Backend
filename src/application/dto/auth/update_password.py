from pydantic import BaseModel, Field


class UpdatePasswordDTO(BaseModel):
    restore_token: str = Field(examples=["5fa3b5da1d384604ae1349c79a32b2f9"])
    password: str = Field(min_length=6, max_length=100, examples=["strong_password"])
