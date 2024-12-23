import uuid
from sqlmodel import SQLModel, Field, ForeignKey


class Privileges(SQLModel, table=True):
    __tablename__ = "privileges"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    teacher_id: uuid.UUID = Field(ForeignKey("teacher.id"))
    privilege: str = Field()
