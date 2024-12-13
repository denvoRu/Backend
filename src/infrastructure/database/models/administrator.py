from sqlalchemy.orm import mapped_column, Mapped
from ..initialize_database import Base


class Administrator(Base):
    __tablename__ = "administrator"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto", nullable=False)
    first_name: Mapped[str] = mapped_column()
    second_name: Mapped[str] = mapped_column()
    third_name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    password: Mapped[str] = mapped_column(nullable=False)