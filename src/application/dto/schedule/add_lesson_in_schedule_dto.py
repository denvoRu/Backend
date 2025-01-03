from src.infrastructure.enums.day_of_week import DayOfWeek
from src.infrastructure.enums.week import Week

from pydantic import BaseModel, Field, UUID4
from datetime import time


class AddLessonInScheduleDTO(BaseModel):
    subject_id: UUID4 = Field(description="id of subject", examples=['d216bd55-4f57-40fa-a6d1-8444f43ccacf'])
    lesson_name: str = Field(min_length=10, max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    speaker_name: str = Field(min_length=10, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    week: Week = Field(default=Week.FIRST, description="number of week for alternate", examples=[Week.FIRST, Week.SECOND])
    day: DayOfWeek = Field(default=DayOfWeek.MONDAY, description="day of week", examples=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY])
    start_time: time = Field(description="time in format HH:MM", examples=["12:00", "13:00"])
    end_time: time = Field(description="time in format HH:MM", examples=["13:30", "15:23"])
