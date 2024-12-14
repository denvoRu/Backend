from sqlmodel import SQLModel, Field

class LessonInfo(SQLModel):
    __tablename__ = "lesson_info"

    lesson_info_id: int = Field(primary_key=True)
    lesson_info_name: str = Field()
