from sqlmodel import SQLModel, Field, ForeignKey, Date
from datetime import date

class TimetableOfDay(SQLModel):
    __tablename__ = "timetable_of_day"

    timetable_id: int = Field(primary_key=True)
    teacher_id: int = Field(ForeignKey("teacher.id"))
    timetable_day: date = Date()
