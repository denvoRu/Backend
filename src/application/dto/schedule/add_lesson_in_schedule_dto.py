from src.infrastructure.enums.day_of_week import DayOfWeek
from src.infrastructure.enums.week import Week
from pydantic import BaseModel, Field


class AddLessonInScheduleDTO(BaseModel):
    subject_id: int = Field(description="id of subject", examples=[1, 2])
    week: Week = Field(default=Week.FIRST, description="number of week for alternate", examples=[Week.FIRST, Week.SECOND])
    day: DayOfWeek = Field(default=DayOfWeek.MONDAY, description="day of week", examples=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY])
    start_time: str = Field(description="time in format HH:MM", examples=["12:00", "13:00"])
    end_time: str = Field(description="time in format HH:MM", examples=["13:30", "15:23"])
