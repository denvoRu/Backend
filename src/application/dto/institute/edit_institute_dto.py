from typing import Optional
from pydantic import BaseModel, Field

class EditInstitudeDTO(BaseModel):
    name: Optional[str] = Field(max_length=100, default=None)
    address: Optional[str] = Field(max_length=100, default=None)
