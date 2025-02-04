from src.infrastructure.config.schedule_time import SCHEDULE_TIME
from src.infrastructure.models.schedule_time import ScheduleTime

from pydantic import BaseModel, Field, field_validator
from datetime import datetime, time, date as dateType


class EditLessonDTO(BaseModel):
    # lesson data transfer fields to edit with examples
    lesson_name: str = Field(default=None, min_length=10, max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    speaker_name: str = Field(default=None, min_length=10, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    start_time: time = Field(default=None, description="time in format HH:MM", examples=["12:00", "13:00"])
    end_time: time = Field(default=None, description="time in format HH:MM", examples=["13:30", "15:23"])
    date: dateType = Field(default=None, description="date in format YYYY-MM-DD", examples=["2023-01-01", "2023-01-02"])

    @field_validator("end_time", mode="after")
    def validate_times(cls, end_time, values):
        time_slot = ScheduleTime(
            start=values.data["start_time"], 
            end=end_time
        )
        if time_slot in SCHEDULE_TIME:
            return end_time
        
        raise ValueError("time must be in range of schedule lessons")

    @field_validator("date")
    def validate_date(cls, date, values):
        now = datetime.now()

        if date < now.date():
            raise ValueError("Date must be in the future")
        
        if date == now.date() and values.data["start_time"] < now.time():
            raise ValueError("Time must be in the future")
            
        return date