import uuid
from sqlmodel import SQLModel, Field, ForeignKey
from decimal import Decimal



class Module(SQLModel, table=True):
    __tablename__ = "module"
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    institute_id: uuid.UUID = Field(ForeignKey("institute.id"))
    name: str = Field(unique=True, nullable=False, index=True)
    rating: Decimal = Field(default=0, max_digits=3, decimal_places=2)
    is_disabled: bool = Field(nullable=False, default=False)
