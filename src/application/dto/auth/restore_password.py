from src.infrastructure.enums.role import Role
from pydantic import BaseModel, EmailStr


class RestorePasswordDTO(BaseModel): 
    email: EmailStr
    role: Role
