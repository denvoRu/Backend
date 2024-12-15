from sqlmodel import SQLModel, Field


class University(SQLModel, table=True):
    __tablename__ = "university"

    id: int = Field(primary_key=True)
    name: str = Field()
