from src.infrastructure.enums.day_of_week import DayOfWeek

from pydantic import BaseModel, Field
from datetime import time
from typing import Optional


class EditLessonInScheduleDTO(BaseModel):
    day: Optional[DayOfWeek] = Field(default=None, description="day of week", examples=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY])
    start_time: Optional[time] = Field(default=None, description="time in format HH:MM", examples=["12:00", "13:00"])
    end_time: Optional[time] = Field(default=None, description="time in format HH:MM", examples=["13:30", "15:23"])
