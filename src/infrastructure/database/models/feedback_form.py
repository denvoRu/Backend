from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class FeedbackForm(SQLModel):
    __tablename__ = "feedback_form"

    id: int = Field(primary_key=True)
    expire_date: time = Time()
    link: str = Field(nullable=False)
    study_group_id = Field(ForeignKey("study_group.id"))
    lesson_id = Field(ForeignKey("lesson.id"))
