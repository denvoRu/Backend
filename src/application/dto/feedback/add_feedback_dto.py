from src.infrastructure.models.tag import Tag
from .extra_fields import ExtraFields

from pydantic import BaseModel, Field, field_serializer, field_validator,  PastDatetime
from typing import List


class AddFeedbackDTO(BaseModel):
    # feedback data transfer fields with examples
    mark: int = Field(gt=0, lt=6)
    student_name: str = Field(default='', min_length=2, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    tags: List[Tag] = Field(default=[], examples=[["понятная", "полезная"]])
    comment: str = Field(default='', examples=["Я бы хотел, чтоб пара длилась меньше"], max_length=300)
    created_at: PastDatetime = Field(examples=["2023-01-01T12:00:00"])
    extra_fields: List[ExtraFields] = Field(default=None, examples=[[ExtraFields(question="Вам понравилась заключительная часть о декораторах?", answer="Да"), ExtraFields(question="Как вам подача материала?", answer="Хорошая")]])


    @field_validator("tags")
    def validate_tags(cls, value):
        tags_unique = set(value)
        if len(tags_unique) != len(value):
            raise ValueError("all tags must be unique")
        return value
    

    @field_serializer("tags", return_type=str, when_used='always')
    def serialize_tags(self, value) -> str:
        return ", ".join(map(lambda x: x.lower(), value))
