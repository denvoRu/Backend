import uuid
from typing import Optional
from sqlmodel import SQLModel, Field, ForeignKey, Date
from datetime import date


class Schedule(SQLModel, table=True):
    __tablename__ = "schedule"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    teacher_id: uuid.UUID = Field(ForeignKey("teacher.id"))
    week_start: Optional[date] = Date()
    is_disabled: bool = Field(nullable=False, default=False)
    