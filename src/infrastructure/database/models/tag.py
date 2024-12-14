from sqlmodel import SQLModel, Field, ForeignKey


class Tag(SQLModel):
    __tablename__ = "tag"

    tag_id: int = Field(primary_key=True)
    tag_name: str = Field()
