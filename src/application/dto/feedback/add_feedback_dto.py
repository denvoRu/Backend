from .extra_fields import ExtraFields

from pydantic import BaseModel, Field, PastDatetime
from typing import List, Optional


class AddFeedbackDTO(BaseModel):
    mark: int = Field(gt=0, lt=6, default=1)
    student_name: str = Field(min_length=2, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    chosen_markers: List[str] = Field(examples=[["понятная", "полезная"]])
    comment: Optional[str] = Field(default=None, examples=["Я бы хотел, чтоб пара длилась меньше"])
    created_at: PastDatetime = Field(examples=["2023-01-01T12:00:00"])
    extra_fields: Optional[List[ExtraFields]] = Field(default=None, examples=[[ExtraFields(question="Вам понравилась заключительная часть о декораторах?", answer="Да"), ExtraFields(question="Как вам подача материала?", answer="Хорошая")]])
