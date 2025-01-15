import uuid
from sqlmodel import SQLModel, Field
from decimal import Decimal


class Institute(SQLModel, table=True):
    __tablename__ = "institute"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str = Field(max_length=100, nullable=False, unique=True)
    short_name: str = Field(max_length=50, nullable=False)
    rating: Decimal = Field(default=0, max_digits=3, decimal_places=2)
    address: str = Field(unique=True, nullable=False)
    is_disabled: bool = Field(nullable=False, default=False)
