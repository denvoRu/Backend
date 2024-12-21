from typing import Optional
from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class Schedule(SQLModel, table=True):
    __tablename__ = "schedule"

    id: int = Field(primary_key=True)
    teacher_id: int = Field(ForeignKey("teacher.id"))
    week_start: Optional[time] = Time()