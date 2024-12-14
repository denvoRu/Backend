from sqlmodel import SQLModel, Field, ForeignKey

class Lesson(SQLModel):
    __tablename__ = "lesson"

    lesson_id: int = Field(primary_key=True)
    timetable_id: int = Field(ForeignKey("timetable_of_day.timetable_id"))
    lesson_info_id: int = Field(ForeignKey("lesson_info.lesson_info_id"))
    lesson_time_id: int = Field(ForeignKey("lesson_time.lesson_time_id"))