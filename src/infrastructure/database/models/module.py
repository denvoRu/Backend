import uuid
from sqlmodel import SQLModel, Field, ForeignKey


class Module(SQLModel, table=True):
    __tablename__ = "module"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    institute_id: uuid.UUID = Field(ForeignKey("institute.id"))
    name: str = Field(unique=True, nullable=False)
    rating: float = Field()
