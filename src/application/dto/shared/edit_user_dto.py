from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class EditUserDTO(BaseModel):
    first_name: Optional[str] = Field(default=None, examples=["Евгений", "Иван"])
    second_name: Optional[str] = Field(default=None, examples=["Смирнов", "Иванов"])
    third_name: Optional[str] = Field(default=None, examples=["Сергеевич", "Иванович"])
    email: Optional[EmailStr] = Field(default=None, examples=["ivanov@example.com", "evgen@example.com"])
    