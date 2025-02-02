from pydantic import BaseModel, Field, UUID4


class AddSubjectDTO(BaseModel):
    # subject data transfer creation fields
    module_id: UUID4 = Field(description="id of module", examples=["d216bd55-4f57-40fa-a6d1-8444f43ccacf"])
    name: str = Field(max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    