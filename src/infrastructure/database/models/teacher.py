import uuid
from sqlmodel import SQLModel, Field, ForeignKey
from decimal import Decimal


class Teacher(SQLModel, table=True):
    __tablename__ = "teacher"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    first_name: str = Field(max_length=100)
    second_name: str = Field(max_length=100)
    third_name: str = Field(max_length=100)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False, min_length=6, max_length=100)
    rating: Decimal = Field(default=0, max_digits=3, decimal_places=2)
    institute_id: uuid.UUID = Field(ForeignKey("institute.id"))
    is_disabled: bool = Field(nullable=False, default=False)
