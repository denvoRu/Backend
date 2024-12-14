from sqlmodel import SQLModel, Field, ForeignKey


class Feedback(SQLModel):
    __tablename__ = "feedback"

    id: int = Field(primary_key=True)
    feedback_form_id: int = Field(ForeignKey("feedback_form.id"))
    mark: int = Field(nullable=False)
    chosen_markers: str = Field()
    comment: str = Field()
    student_name: str = Field(nullable=False)
