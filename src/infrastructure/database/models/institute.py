import uuid
from sqlmodel import SQLModel, Field


class Institute(SQLModel, table=True):
    __tablename__ = "institute"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    name: str = Field(max_length=100, nullable=False, unique=True)
    short_name: str = Field(max_length=50, nullable=False)
    rating: float = Field(nullable=False, default=0)
    address: str = Field(unique=True, nullable=False)
