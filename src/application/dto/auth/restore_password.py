from src.infrastructure.enums.role import Role
from pydantic import BaseModel, EmailStr, Field


class RestorePasswordDTO(BaseModel): 
    email: EmailStr = Field(examples=["evgen@example.com", "ivanov@example.com"])
    role: Role = Field(default=Role.TEACHER, examples=["teacher", "admin"])
