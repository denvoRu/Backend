from pydantic import BaseModel, Field
from typing import Optional


class EditModuleDTO(BaseModel):
    # module data transfer creation fields with examples
    name: Optional[str] = Field(max_length=100, examples=["Современные языки программирования", "Математический анализ"], default=None)
    