from sqlmodel import SQLModel, Field, ForeignKey


class Teacher(SQLModel):
    __tablename__ = "teacher"

    id: int = Field(primary_key=True)
    first_name: str = Field()
    second_name: str = Field()
    third_name: str = Field()
    email: str = Field(unique=True, nullable=False, index=True)
    password: str = Field(nullable=False)