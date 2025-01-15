from pydantic import BaseModel, EmailStr, Field


class EditUserDTO(BaseModel):
    # user data transfer fields for edit
    first_name: str = Field(default=None, examples=["Евгений", "Иван"])
    second_name: str = Field(default=None, examples=["Смирнов", "Иванов"])
    third_name: str = Field(default=None, examples=["Сергеевич", "Иванович"])
    password: str = Field(default=None, min_length=6, max_length=100, examples=["strong_password"])
    email: EmailStr = Field(default=None, examples=["ivanov@example.com", "evgen@example.com"])
    