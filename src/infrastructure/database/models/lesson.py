import uuid
from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class Lesson(SQLModel, table=True):
    __tablename__ = "lesson"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    date: time = Time()
    study_group_id: uuid.UUID = Field(ForeignKey("study_group.id"))
