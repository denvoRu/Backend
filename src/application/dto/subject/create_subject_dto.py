from pydantic import BaseModel, Field


class CreateSubjectDTO(BaseModel):
    institute_id: int = Field(description="id of institute", examples=[1, 2])
    module_id: int = Field(description="id of module", examples=[1, 2])
    name: str = Field(max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    