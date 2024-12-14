from sqlmodel import SQLModel, Field, ForeignKey


class Privileges(SQLModel):
    __tablename__ = "privileges"

    id: int = Field(primary_key=True)
    teacher_id: int = Field(ForeignKey("teacher.id"))
    privilege: str = Field()
