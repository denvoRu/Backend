from pydantic import BaseModel, Field, UUID4, FutureDate
from typing import List


class EditConstLinkDTO(BaseModel):
    end_date: FutureDate = Field(description="date in format YYYY-MM-DD", examples=["2023-01-01", "2023-01-02"])
