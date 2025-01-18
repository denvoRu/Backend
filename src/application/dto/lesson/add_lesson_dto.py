from src.infrastructure.config.schedule_time import SCHEDULE_TIME
from src.infrastructure.models.schedule_time import ScheduleTime
from src.infrastructure.enums.week import Week

from pydantic import BaseModel, Field, validator, UUID4
from datetime import time, date as dateType


class AddLessonDTO(BaseModel):
    # lesson data transfer add fields
    subject_id: UUID4 = Field(description="id of subject", examples=['d216bd55-4f57-40fa-a6d1-8444f43ccacf'])
    lesson_name: str = Field(min_length=2, max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    speaker_name: str = Field(min_length=2, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    date: dateType = Field(description="date in format YYYY-MM-DD", examples=["2023-01-01", "2023-01-02"])
    start_time: time = Field(description="time in format HH:MM", examples=["12:00", "13:00"])
    end_time: time = Field(description="time in format HH:MM", examples=["13:30", "15:23"])

