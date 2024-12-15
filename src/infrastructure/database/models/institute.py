from sqlmodel import SQLModel, Field


class Institute(SQLModel, table=True):
    __tablename__ = "institute"

    id: int = Field(primary_key=True)
    name: str = Field(max_length=100,nullable=False)
    short_name: str = Field(max_length=50, nullable=False)
    rating: float = Field()
    address: str = Field()

