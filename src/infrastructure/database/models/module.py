from sqlmodel import SQLModel, Field, ForeignKey


class Module(SQLModel, table=True):
    __tablename__ = "module"
    id: int = Field(primary_key=True)
    institute_id: int = Field(ForeignKey("institute.id"))
    name: str = Field()
    rating: float = Field()
