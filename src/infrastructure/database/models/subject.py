from sqlmodel import SQLModel, Field, ForeignKey


class Subject(SQLModel, table=True):
    __tablename__ = "subject"

    id: int = Field(primary_key=True)
    institute_id: int = Field(ForeignKey("institute.id"))
    name: str = Field()
    rating: float = Field()
