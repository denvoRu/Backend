import uuid
from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class ScheduleLesson(SQLModel, table=True):
    __tablename__ = "schedule_lesson"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    schedule_id: uuid.UUID = Field(ForeignKey("schedule.id"))
    subject_id: uuid.UUID = Field(ForeignKey("subject.id"))
    week: int = Field()
    day: int = Field()
    start_time: time = Time()
    end_time: time = Time()
    