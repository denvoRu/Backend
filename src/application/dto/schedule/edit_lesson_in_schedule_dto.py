from src.infrastructure.enums.week import Week
from src.infrastructure.enums.day_of_week import DayOfWeek

from pydantic import BaseModel, UUID4, Field, validator
from datetime import date


class EditLessonInScheduleDTO(BaseModel):
    # lesson data transfer edit fields
    subject_id: UUID4 = Field(default=None, description="id of subject", examples=["d216bd55-4f57-40fa-a6d1-8444f43ccacf"])
    day: DayOfWeek = Field(default=None, description="day of week", examples=[DayOfWeek.MONDAY, DayOfWeek.TUESDAY])
    lesson_name: str = Field(default=None, max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    speaker_name: str = Field(default=None, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    week: Week = Field(default=None, description="number of week for alternate", examples=[Week.FIRST, Week.SECOND])
    end_date: date = Field(default=None, description="date in format YYYY-MM-DD", examples=["2023-01-01", "2023-01-02"])

    @validator("end_date")
    def validate_end_date(cls, value):
        if value >= date.today():
            return value
        
        raise ValueError("end date must be in future")
    