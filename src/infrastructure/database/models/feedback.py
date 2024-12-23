import uuid
from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class Feedback(SQLModel, table=True):
    __tablename__ = "feedback"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    lesson_id: uuid.UUID = Field(ForeignKey("lesson.id"))
    student_name: str = Field()
    mark: int = Field(nullable=False)
    chosen_markers: str = Field(nullable=False)
    comment: str = Field()
    created_at: time = Time()
    is_disabled: bool = Field(nullable=False, default=False)

