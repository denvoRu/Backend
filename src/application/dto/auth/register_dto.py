from src.infrastructure.enums.role import Role
from typing import Optional
from pydantic import BaseModel, Field, EmailStr


class RegisterDTO(BaseModel):
    first_name: str = Field(examples=["Евгений", "Иван"])
    second_name: str = Field(examples=["Смирнов", "Иванов"])
    third_name: str = Field(examples=["Сергеевич", "Иванович"])
    email: EmailStr = Field(examples=["ivanov@example.com", "evgen@example.com"])
    institute_id: Optional[int] = Field(default=None, examples=[1, 2], description="id of institute for teacher")
    password: str = Field(min_length=6, max_length=100, examples=["strong_password"])
    role: Role = Field(default=Role.TEACHER, examples=["teacher", "admin"])
