from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class ScheduleLesson(SQLModel, table=True):
    __tablename__ = "schedule_lesson"

    id: int = Field(primary_key=True)
    schedule_id: int = Field(ForeignKey("schedule.id"))
    subject_id: int = Field(ForeignKey("subject.id"))
    week: int = Field()
    day: int = Field()
    start_time: time = Time()
    end_time: time = Time()