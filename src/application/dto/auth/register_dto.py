from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from src.infrastructure.enums.role import Role


class RegisterDTO(BaseModel):
    first_name: str
    second_name: str
    third_name: str
    email: EmailStr
    institute_id: Optional[int]
    password: str = Field(min_length=6, max_length=100)
    role: Role = Field(default=Role.TEACHER)