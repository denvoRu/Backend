from sqlmodel import SQLModel, Field


class Module(SQLModel, table=True):
    __tablename__ = "module"

    id: int = Field(primary_key=True)
    name: str = Field()
    rating: float = Field()
