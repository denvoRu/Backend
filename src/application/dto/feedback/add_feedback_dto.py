from pydantic import BaseModel, Field
from typing import List, Optional


class AddFeedbackDTO(BaseModel):
    mark: int = Field(gt=0, lt=6)
    full_name: str = Field(
        min_length=2,
        max_length=100, 
        examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"]
    )
    chosen_markers: List[str] = Field(
        examples=[
            ["понятная", "полезная"],
        ]
    )
    comment: Optional[str] = Field(
        default=None, 
        examples=["Я бы хотел, чтоб пара длилась меньше"]
    )
    extra_fields: dict = Field(
        default=None, 
        examples=[
            {
                "Вам понравилась заключительная часть о декораторах?": "Да", 
                "Как вам подача материала?": "Хорошая"
            }
        ]
    )
