from sqlmodel import SQLModel, Field, ForeignKey


class StudyGroup(SQLModel):
    __tablename__ = "study_group"

    id: int = Field(primary_key=True)
    subject_id: int = Field(ForeignKey("subject.id"))
    teacher_id: int = Field(ForeignKey("teacher.id"))
