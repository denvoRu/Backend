from pydantic import BaseModel, Field


class EditSubjectDTO(BaseModel):
    # subject data transfer edit fields
    name: str = Field(default=None, max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    