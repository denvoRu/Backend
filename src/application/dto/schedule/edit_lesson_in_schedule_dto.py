from src.infrastructure.enums.day_of_week import DayOfWeek
from pydantic import BaseModel, Field
from datetime import time
from typing import Optional


class EditLessonInScheduleDTO(BaseModel):
    subject_id: Optional[int] = Field(default=None)
    day: Optional[DayOfWeek] = Field(default=None)
    start_time: Optional[time] = Field(default=None)
    end_time: Optional[time] = Field(default=None)