import uuid
from sqlmodel import SQLModel, Field, ForeignKey


class ExtraFieldSetting(SQLModel, table=True):
    __tablename__ = "extra_field_setting"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    lesson_id: uuid.UUID = Field(ForeignKey("lesson.id"))
    extra_field_name: str = Field(nullable=False, max_length=300)
    is_disabled: bool = Field(nullable=False, default=False)