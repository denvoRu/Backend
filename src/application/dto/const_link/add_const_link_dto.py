from pydantic import BaseModel, Field, UUID4, FutureDate
from typing import List


class AddConstLinkDTO(BaseModel):
    subject_id: UUID4 = Field(description="id of subject", examples=["d216bd55-4f57-40fa-a6d1-8444f43ccacf"])
    teacher_id: UUID4 = Field(description="id of teacher", examples=["d216bd55-4f57-40fa-a6d1-8444f43ccacf"])
    end_date: FutureDate = Field(description="date in format YYYY-MM-DD", examples=["2023-01-01", "2023-01-02"])
