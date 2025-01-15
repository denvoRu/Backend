import uuid
from sqlmodel import SQLModel, Field, ForeignKey
from decimal import Decimal


class Subject(SQLModel, table=True):
    __tablename__ = "subject"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    module_id: uuid.UUID = Field(ForeignKey("module.id"))
    name: str = Field(unique=True, nullable=False, index=True)
    rating: Decimal = Field(default=0, max_digits=3, decimal_places=2)
    is_disabled: bool = Field(nullable=False, default=False)
