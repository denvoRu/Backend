from .extra_fields import ExtraFields

from pydantic import BaseModel, Field
from typing import List, Optional


class AddFeedbackDTO(BaseModel):
    mark: int = Field(gt=0, lt=6, default=1)
    full_name: str = Field(min_length=2, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    chosen_markers: List[str] = Field(examples=[["понятная", "полезная"]])
    comment: Optional[str] = Field(default=None, examples=["Я бы хотел, чтоб пара длилась меньше"])
    extra_fields: Optional[List[ExtraFields]] = Field(default=None, examples=[[ExtraFields(question="Вам понравилась заключительная часть о декораторах?", answer="Да"), ExtraFields(question="Как вам подача материала?", answer="Хорошая")]])
