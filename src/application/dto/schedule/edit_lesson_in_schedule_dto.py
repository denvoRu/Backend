from src.infrastructure.enums.day_of_week import DayOfWeek
from pydantic import BaseModel, Field
from datetime import time
from typing import Optional


class EditLessonInScheduleDTO(BaseModel):
    subject_id: int = Field(default=None, description="id of subject", examples=[1, 2])
    day: DayOfWeek = Field(default=None, description="day of week", examples=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY])
    start_time: str = Field(default=None, description="time in format HH:MM", examples=["12:00", "13:00"])
    end_time: str = Field(default=None, description="time in format HH:MM", examples=["13:30", "15:23"])
