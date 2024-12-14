from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class Lesson(SQLModel):
    __tablename__ = "lesson"

    id: int = Field(primary_key=True)
    date: time = Time()
    study_group_id: int = Field(ForeignKey("study_group.id"))
