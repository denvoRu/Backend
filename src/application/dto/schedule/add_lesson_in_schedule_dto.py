from src.infrastructure.enums.day_of_week import DayOfWeek
from pydantic import BaseModel


class AddLessonInScheduleDTO(BaseModel):
    subject_id: int
    week: int
    day: DayOfWeek
    start_time: str
    end_time: str