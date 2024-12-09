from sqlalchemy import Time
from sqlalchemy.orm import mapped_column, Mapped
from ..initialize_database import Base


class LessonTime(Base):
    __tablename__ = "lesson_time"

    lesson_time_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True, nullable=False)
    lesson_time_start: Mapped[Time] = mapped_column()
    lesson_time_end: Mapped[Time] = mapped_column()
