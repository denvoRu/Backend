from pydantic import BaseModel, Field


class CreateModuleDTO(BaseModel):
    institute_id: int = Field(description="id of institute", examples=[1, 2])
    name: str = Field(max_length=100, examples=["Современные языки программирования", "Математический анализ"])
    