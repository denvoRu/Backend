import uuid
from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class Feedback(SQLModel, table=True):
    __tablename__ = "feedback"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    lesson_id: uuid.UUID = Field(ForeignKey("lesson.id"), index=True)
    student_name: str = Field(max_length=100, nullable=False)
    mark: int = Field(nullable=False)
    tags: str = Field(nullable=False)
    comment: str = Field(max_length=250)
    created_at: time = Time()
    is_disabled: bool = Field(nullable=False, default=False)

