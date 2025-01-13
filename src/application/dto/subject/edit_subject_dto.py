from pydantic import BaseModel, Field
from typing import Optional


class EditSubjectDTO(BaseModel):
    # subject data transfer edit fields
    name: Optional[str] = Field(max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"], default=None)
    