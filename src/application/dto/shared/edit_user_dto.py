from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class EditUserDTO(BaseModel):
    first_name: Optional[str] = Field(default=None)
    second_name: Optional[str] = Field(default=None)
    third_name: Optional[str] = Field(default=None)
    email: Optional[EmailStr] = Field(default=None)