from pydantic import BaseModel, Field


class EditSubjectDTO(BaseModel):
    name: str = Field(max_length=100)
    