import uuid
from sqlmodel import SQLModel, Field, ForeignKey


class Feedback(SQLModel, table=True):
    __tablename__ = "feedback"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    feedback_form_id: uuid.UUID = Field(ForeignKey("feedback_form.id"))
    mark: int = Field(nullable=False)
    chosen_markers: str = Field()
    comment: str = Field()
    student_name: str = Field(nullable=False)
