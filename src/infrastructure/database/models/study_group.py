import uuid
from sqlmodel import SQLModel, Field, ForeignKey
from decimal import Decimal


class StudyGroup(SQLModel, table=True):
    __tablename__ = "study_group"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    subject_id: uuid.UUID = Field(ForeignKey("subject.id"))
    teacher_id: uuid.UUID = Field(ForeignKey("teacher.id"))
    is_disabled: bool = Field(nullable=False, default=False)
    rating: Decimal = Field(default=0, max_digits=3, decimal_places=2)