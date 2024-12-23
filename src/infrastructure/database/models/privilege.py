import uuid
from sqlmodel import SQLModel, Field, ForeignKey


class Privilege(SQLModel, table=True):
    __tablename__ = "privilege"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    teacher_id: uuid.UUID = Field(ForeignKey("teacher.id"))
    name: str = Field()
