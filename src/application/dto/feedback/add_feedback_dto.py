from src.infrastructure.models.tag import Tag
from .extra_fields import ExtraFields

from pydantic import BaseModel, Field, field_serializer, PastDatetime
from typing import List, Optional


class AddFeedbackDTO(BaseModel):
    # feedback data transfer fields with examples
    mark: int = Field(gt=0, lt=6)
    # student_name: str = Field(default=None, min_length=2, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    tags: Optional[List[Tag]] = Field(examples=[["понятная", "полезная"]])
    comment: Optional[str] = Field(default=None, examples=["Я бы хотел, чтоб пара длилась меньше"])
    created_at: PastDatetime = Field(examples=["2023-01-01T12:00:00"])
    extra_fields: Optional[List[ExtraFields]] = Field(default=None, examples=[[ExtraFields(question="Вам понравилась заключительная часть о декораторах?", answer="Да"), ExtraFields(question="Как вам подача материала?", answer="Хорошая")]])

    @field_serializer("tags", return_type=str, when_used='always')
    def serialize_tags(self, value) -> str:
        return ", ".join(map(lambda x: x.lower(), value))
