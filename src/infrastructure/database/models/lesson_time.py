from datetime import time
from sqlmodel import SQLModel, Field, Time, Column

class LessonTime(SQLModel):
    __tablename__ = "lesson_time"

    lesson_time_id: int = Field(primary_key=True)
    lesson_time_start: time = Time()
    lesson_time_end: time = Time()
