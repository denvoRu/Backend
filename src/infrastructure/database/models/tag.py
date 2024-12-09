from sqlalchemy.orm import mapped_column, Mapped
from ..initialize_database import Base


class Tag(Base):
    __tablename__ = "tag"

    tag_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True, nullable=False)
    tag_name: Mapped[str] = mapped_column()
