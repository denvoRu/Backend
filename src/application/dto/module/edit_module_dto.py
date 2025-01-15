from pydantic import BaseModel, Field


class EditModuleDTO(BaseModel):
    # module data transfer creation fields with examples
    name: str = Field(default=None, max_length=100, examples=["Современные языки программирования", "Математический анализ"])
    