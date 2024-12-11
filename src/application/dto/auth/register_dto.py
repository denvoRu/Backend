from pydantic import BaseModel, Field, EmailStr
from src.domain.enums.role import Role


class RegisterDTO(BaseModel):
    first_name: str
    second_name: str
    third_name: str
    username: EmailStr
    password: str = Field(min_length=6, max_length=100)
    role: Role = Field(default=Role.TEACHER)