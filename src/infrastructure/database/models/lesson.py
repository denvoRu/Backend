import uuid
from sqlmodel import SQLModel, Field, ForeignKey, Time, Date
from datetime import time, date as DateType


class Lesson(SQLModel, table=True):
    __tablename__ = "lesson"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    study_group_id: uuid.UUID = Field(ForeignKey("study_group.id"))
    lesson_name: str = Field(nullable=False)
    speaker_name: str = Field(nullable=False)
    rating: float = Field(nullable=False, default=0.0)
    date: DateType = Date()
    start_time: time = Time()
    end_time: time = Time()
    is_disabled: bool = Field(nullable=False, default=False)
    study_group_access: bool = Field(nullable=False, default=False)
