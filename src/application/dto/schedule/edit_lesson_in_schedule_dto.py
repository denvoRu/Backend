from src.infrastructure.enums.day_of_week import DayOfWeek

from pydantic import BaseModel, UUID4, Field
from datetime import time



class EditLessonInScheduleDTO(BaseModel):
    # lesson data transfer edit fields
    subject_id: UUID4 = Field(default=None, description="id of subject", examples=['d216bd55-4f57-40fa-a6d1-8444f43ccacf'])
    day: DayOfWeek = Field(default=None, description="day of week", examples=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY])
    lesson_name: str = Field(default=None, max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    speaker_name: str = Field(default=None, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    start_time: time = Field(default=None, description="time in format HH:MM", examples=["12:00", "13:00"])
    end_time: time = Field(default=None, description="time in format HH:MM", examples=["13:30", "15:23"])