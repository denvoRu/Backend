from sqlmodel import SQLModel, Field, ForeignKey



class ReviewTag(SQLModel):
    __tablename__ = "review_tag"

    review_tag_id: int = Field(primary_key=True)
    tag_id: int = Field(ForeignKey("tag.tag_id"))
    review_id: int = Field(ForeignKey("review.review_id"))
