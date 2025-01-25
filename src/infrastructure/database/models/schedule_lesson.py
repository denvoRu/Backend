import uuid
from sqlmodel import SQLModel, Field, ForeignKey, Time, Date
from datetime import time, date


class ScheduleLesson(SQLModel, table=True):
    __tablename__ = "schedule_lesson"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    schedule_id: uuid.UUID = Field(ForeignKey("schedule.id"))
    lesson_name: str = Field(nullable=False)
    speaker_name: str = Field(nullable=False)
    subject_id: uuid.UUID = Field(ForeignKey("subject.id"))
    week: int = Field()
    day: int = Field()
    start_time: time = Time()
    end_time: time = Time()
    end_date: date = Date()
    