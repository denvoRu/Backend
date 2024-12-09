from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from ..initialize_database import Base


class Review(Base):
    __tablename__ = "review"

    review_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True, nullable=False)
    lesson_id: Mapped[int] = mapped_column(ForeignKey("lesson.lesson_id"))
    review_mark: Mapped[int] = mapped_column()
    review_description: Mapped[str] = mapped_column()
