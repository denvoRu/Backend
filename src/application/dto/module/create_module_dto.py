from pydantic import BaseModel


class CreateModuleDTO(BaseModel):
    name: str