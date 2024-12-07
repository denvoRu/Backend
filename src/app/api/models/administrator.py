from sqlalchemy.orm import mapped_column, Mapped
from src.database.initialize_database import Base


class Administrator(Base):
    __tablename__ = "administrator"

    administrator_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True, nullable=False)
    administrator_first_name: Mapped[str] = mapped_column()
    administrator_second_name: Mapped[str] = mapped_column()
    administrator_third_name: Mapped[str] = mapped_column()
    administrator_email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)
    administrator_password: Mapped[str] = mapped_column(nullable=False)