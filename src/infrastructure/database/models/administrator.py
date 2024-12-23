import uuid
from sqlmodel import SQLModel, Field


class Administrator(SQLModel, table=True):
    __tablename__ = "administrator"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    first_name: str = Field(max_length=100)
    second_name: str = Field(max_length=100)
    third_name: str = Field(max_length=100)
    email: str = Field(unique=True, nullable=False)
    password: str = Field(nullable=False, min_length=6, max_length=100)
