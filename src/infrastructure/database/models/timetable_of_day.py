from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import mapped_column, Mapped
from ..initialize_database import Base


class TimetableOfDay(Base):
    __tablename__ = "timetable_of_day"

    timetable_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True, nullable=False)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id"))
    timetable_day = Date()
