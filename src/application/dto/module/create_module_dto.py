from pydantic import BaseModel, Field, UUID4


class CreateModuleDTO(BaseModel):
    institute_id: UUID4 = Field(description="id of institute", examples=['d216bd55-4f57-40fa-a6d1-8444f43ccacf'])
    name: str = Field(max_length=100, examples=["Современные языки программирования", "Математический анализ"])
    