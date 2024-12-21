from pydantic import BaseModel, Field


class CreateModuleDTO(BaseModel):
    name: str = Field(max_length=100, examples=["Современные языки программирования", "Математический анализ"])
    