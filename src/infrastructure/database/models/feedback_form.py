import uuid
from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class FeedbackForm(SQLModel, table=True):
    __tablename__ = "feedback_form"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    expire_date: time = Time()
    link: str = Field(nullable=False)
    study_group_id: uuid.UUID = Field(ForeignKey("study_group.id"))
    lesson_id: uuid.UUID = Field(ForeignKey("lesson.id"))
