from src.infrastructure.enums.role import Role

from typing import List
from pydantic import BaseModel, Field, EmailStr, UUID4


class RegisterDTO(BaseModel):
    # register data transfer info with examples
    first_name: str = Field(examples=["Евгений", "Иван"])
    second_name: str = Field(examples=["Смирнов", "Иванов"])
    third_name: str = Field(examples=["Сергеевич", "Иванович"])
    email: EmailStr = Field(examples=["ivanov@example.com", "evgen@example.com"])
    institute_id: UUID4 = Field(default=None, examples=["d216bd55-4f57-40fa-a6d1-8444f43ccacf"], description="id of institute for teacher")
    password: str = Field(min_length=6, max_length=100, examples=["strong_password"])
    role: Role = Field(default=Role.TEACHER, examples=["teacher", "admin"])
    subjects: List[UUID4] = Field(default=[], examples=[["d216bd55-4f57-40fa-a6d1-8444f43ccacf", "d216bd55-4f57-40fa-a6d1-8444f43ccacf"]])
