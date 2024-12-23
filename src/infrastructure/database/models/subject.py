import uuid
from sqlmodel import SQLModel, Field, ForeignKey


class Subject(SQLModel, table=True):
    __tablename__ = "subject"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    module_id: uuid.UUID = Field(ForeignKey("module.id"))
    name: str = Field(unique=True, nullable=False)
    rating: float = Field()
