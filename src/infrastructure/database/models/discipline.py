from sqlmodel import SQLModel, Field


class Discipline(SQLModel, table=True):
    __tablename__ = "discipline"

    id: int = Field(primary_key=True)
    name: str = Field()
    rating: float = Field()
