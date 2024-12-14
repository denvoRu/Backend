from sqlmodel import SQLModel, Field, ForeignKey


class Review(SQLModel):
    __tablename__ = "review"

    review_id: int = Field(primary_key=True)
    lesson_id: int = Field(ForeignKey("lesson.lesson_id"))
    review_mark: int = Field()
    review_description: str = Field()
