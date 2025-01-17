from src.infrastructure.enums.day_of_week import DayOfWeek
from src.infrastructure.enums.week import Week
from src.infrastructure.config.schedule_time import SCHEDULE_TIME
from src.infrastructure.models.schedule_time import ScheduleTime

from pydantic import BaseModel, Field, validator, UUID4
from datetime import time, date


class AddLessonInScheduleDTO(BaseModel):
    # lesson data transfer add fields
    subject_id: UUID4 = Field(description="id of subject", examples=['d216bd55-4f57-40fa-a6d1-8444f43ccacf'])
    lesson_name: str = Field(min_length=10, max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    speaker_name: str = Field(min_length=10, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    week: Week = Field(default=Week.FIRST, description="number of week for alternate", examples=[Week.FIRST, Week.SECOND])
    day: DayOfWeek = Field(default=DayOfWeek.MONDAY, description="day of week", examples=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY])
    start_time: time = Field(description="time in format HH:MM", examples=["12:00", "13:00"])
    end_time: time = Field(description="time in format HH:MM", examples=["13:30", "15:23"])
    end_date: date = Field(description="date in format YYYY-MM-DD", examples=["2023-01-01", "2023-01-02"])

    @validator("end_date")
    def validate_end_date(cls, value):
        if value >= date.today():
            return value
        
        raise ValueError("end date must be in future")
    

    @validator("start_time", "end_time")
    def validate_time(cls, value):
        if ScheduleTime(start=value[0], end=value[1]) in SCHEDULE_TIME:
            return value
        
        raise ValueError("time must be in schedule time")
    