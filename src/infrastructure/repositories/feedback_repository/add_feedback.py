from src.infrastructure.database import (
    ExtraField, ExtraFieldSetting, Feedback, add_instance, commit_rollback, db
)

from sqlalchemy import select
from uuid import UUID
from typing import List


async def add(lesson_id: UUID, dto: dict):
    feedback = Feedback(
        lesson_id=lesson_id, 
        **dto
    )
    await add_instance(feedback)
    return feedback.id


async def add_extra_fields(
    lesson_id: UUID, 
    feedback_id: UUID, 
    dto_list: List[dict]
):
    for i in dto_list: 
        extra_field_id = select(ExtraFieldSetting.id).where(
            ExtraFieldSetting.lesson_id == lesson_id, 
            ExtraFieldSetting.extra_field_name == i["question"]
        )
        extra_field = ExtraField(
            feedback_id=feedback_id,
            extra_field_setting_id=extra_field_id,
            value=i["answer"]
        )
        db.add(extra_field)

    await commit_rollback()
