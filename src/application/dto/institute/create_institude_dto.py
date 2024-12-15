from pydantic import BaseModel, Field

class CreateInstitudeDTO(BaseModel):
    name: str = Field(max_length=100)
    address: str = Field(max_length=100)
