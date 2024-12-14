from sqlmodel import SQLModel, Field


class Administrator(SQLModel, table=True):
    __tablename__ = "administrator"

    id: int = Field(primary_key=True)
    first_name: str = Field(max_length=100)
    second_name: str = Field(max_length=100)
    third_name: str = Field(max_length=100)
    email: str = Field(unique=True, nullable=False, index=True)
    password: str = Field(nullable=False, min_length=6, max_length=100)
