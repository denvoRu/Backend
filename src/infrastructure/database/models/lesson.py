from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from ..initialize_database import Base


class Lesson(Base):
    __tablename__ = "lesson"

    lesson_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True, nullable=False)
    timetable_id: Mapped[int] = mapped_column(ForeignKey("timetable_of_day.timetable_id"))
    lesson_info_id: Mapped[int] = mapped_column(ForeignKey("lesson_info.lesson_info_id"))
    lesson_time_id: Mapped[int] = mapped_column(ForeignKey("lesson_time.lesson_time_id"))