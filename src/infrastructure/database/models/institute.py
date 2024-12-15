from sqlmodel import SQLModel, Field, ForeignKey


class Institute(SQLModel, table=True):
    __tablename__ = "institute"

    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    rating: float = Field()
    address: str = Field()

