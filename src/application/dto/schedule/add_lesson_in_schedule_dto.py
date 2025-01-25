from src.infrastructure.enums.day_of_week import DayOfWeek
from src.infrastructure.enums.week import Week
from src.infrastructure.config.schedule_time import SCHEDULE_TIME
from src.infrastructure.models.schedule_time import ScheduleTime

from pydantic import BaseModel, Field, field_validator, UUID4
from typing_extensions import Union, Literal
from datetime import time, date


class AddLessonInScheduleDTO(BaseModel):
    # lesson data transfer add fields
    subject_id: UUID4 = Field(description="id of subject", examples=["d216bd55-4f57-40fa-a6d1-8444f43ccacf"])
    lesson_name: str = Field(min_length=2, max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    speaker_name: str = Field(min_length=2, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    week: Union[Week, Literal["all"]] = Field(default="all", description="number of week for alternate", examples=[Week.FIRST, Week.SECOND])
    day: DayOfWeek = Field(default=DayOfWeek.MONDAY, description="day of week", examples=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY])
    start_time: time = Field(description="time in format HH:MM", examples=["12:00", "13:00"])
    end_time: time = Field(description="time in format HH:MM", examples=["13:30", "15:23"])
    end_date: date = Field(description="date in format YYYY-MM-DD", examples=["2023-01-01", "2023-01-02"])


    @field_validator("end_time", mode="after")
    def validate_times(cls, end_time, values):
        time_slot = ScheduleTime(
            start=values.data["start_time"], 
            end=end_time
        )
        if time_slot in SCHEDULE_TIME:
            return end_time
        
        raise ValueError("time must be in range of schedule lessons")
