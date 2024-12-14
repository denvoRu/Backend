from sqlalchemy.orm import mapped_column, Mapped
from ..initialize_database import Base


class Privileges(Base):
    __tablename__ = "privileges"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement="auto", nullable=False)
    teacher_id: Mapped[int]
    privilage: Mapped[str]