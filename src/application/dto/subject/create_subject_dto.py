from pydantic import BaseModel, Field


class CreateSubjectDTO(BaseModel):
    institute_id: int = Field()
    module_id: int = Field()
    name: str = Field(max_length=100)
    