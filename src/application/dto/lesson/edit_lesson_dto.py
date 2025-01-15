from pydantic import BaseModel, Field
from datetime import time


class EditLessonDTO(BaseModel):
    # lesson data transfer fields to edit with examples
    lesson_name: str = Field(default=None, min_length=10, max_length=100, examples=["Разработка на Python (FastAPI)", "Javascript (React)"])
    speaker_name: str = Field(default=None, min_length=10, max_length=100, examples=["Смирнов Евгений Сергеевич", "Иванов Иван Иванович"])
    end_time: time = Field(default=None, description="time in format HH:MM", examples=["13:30", "15:23"])
