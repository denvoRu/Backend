import uuid
from sqlmodel import SQLModel, Field, ForeignKey, DateTime
from datetime import datetime


class Feedback(SQLModel, table=True):
    __tablename__ = "feedback"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    lesson_id: uuid.UUID = Field(ForeignKey("lesson.id"), index=True)
    student_name: str = Field(max_length=100, nullable=False)
    mark: int = Field(nullable=False)
    tags: str = Field(nullable=False)
    comment: str = Field(max_length=300)
    created_at: datetime = DateTime()
    is_disabled: bool = Field(nullable=False, default=False)

