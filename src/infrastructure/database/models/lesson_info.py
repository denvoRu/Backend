from sqlalchemy.orm import mapped_column, Mapped
from ..initialize_database import Base


class LessonInfo(Base):
    __tablename__ = "lesson_info"

    lesson_info_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True, nullable=False)
    lesson_info_name: Mapped[str] = mapped_column()
