from sqlalchemy.orm import mapped_column, Mapped
from src.database.initialize_database import Base


class Teacher(Base):
    __tablename__ = "teacher"

    teacher_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True, nullable=False)
    teacher_first_name: Mapped[str] = mapped_column()
    teacher_second_name: Mapped[str] = mapped_column()
    teacher_third_name: Mapped[str] = mapped_column()
    teacher_email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    teacher_password: Mapped[str] = mapped_column(nullable=False)