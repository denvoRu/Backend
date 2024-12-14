from sqlmodel import SQLModel, Field, ForeignKey


class TeacherSubject(SQLModel):
    __tablename__ = "teacher_subject"

    id: int = Field(primary_key=True)
    subject_id: int = Field(ForeignKey("subject.id"))
    teacher_id: int = Field(ForeignKey("teacher.id"))
