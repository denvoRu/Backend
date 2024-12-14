from sqlmodel import SQLModel, Field, ForeignKey


class Institute(SQLModel):
    __tablename__ = "institute"

    id: int = Field(primary_key=True)
    name: str = Field(nullable=False)
    rating: float = Field()
    address: str = Field()
    university_id: int = Field(ForeignKey("university.id"))
