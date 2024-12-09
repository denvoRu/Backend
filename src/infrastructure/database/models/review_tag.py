from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped
from ..initialize_database import Base


class ReviewTag(Base):
    __tablename__ = "review_tag"

    review_tag_id: Mapped[int] = mapped_column(primary_key=True, auto_increment=True, nullable=False)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tag.tag_id"))
    review_id: Mapped[int] = mapped_column(ForeignKey("review.review_id"))
