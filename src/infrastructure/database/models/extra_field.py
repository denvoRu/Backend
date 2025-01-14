import uuid
from sqlmodel import SQLModel, Field, ForeignKey, Time
from datetime import time


class ExtraField(SQLModel, table=True):
    __tablename__ = "extra_field"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True, index=True)
    feedback_id: uuid.UUID = Field(ForeignKey("feedback.id"))
    extra_field_setting_id: uuid.UUID = Field(ForeignKey("extra_field_setting.id"))
    value: str = Field(nullable=False, max_length=300)