from pydantic import BaseModel

class UpdatePasswordDTO(BaseModel):
    restore_token: str
    password: str