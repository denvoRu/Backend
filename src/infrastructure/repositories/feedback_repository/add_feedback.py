from src.infrastructure.database import (
    ExtraField, ExtraFieldSetting, Feedback, add_instance, db
)

from sqlalchemy import select
from uuid import UUID
from typing import List


async def add(lesson_id: UUID, dto: dict):
    """
    Add a feedback
    :param lesson_id: lesson to add feedback to
    :param dto: feedback details
    """
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
    """
    Add extra fields to a feedback
    :param lesson_id: lesson
    :param feedback_id: feedback to add extra fields to
    """
    for i in dto_list: 
        extra_field_id = select(ExtraFieldSetting.id).where(
            ExtraFieldSetting.lesson_id == lesson_id, 
            ExtraFieldSetting.extra_field_name == i["question"]
        )
        extra_field_id = await db.execute(extra_field_id)
        extra_field_id = extra_field_id.scalar()
        
        if not extra_field_id:
            raise Exception("Extra field not found")

        extra_field = ExtraField(
            feedback_id=feedback_id,
            extra_field_setting_id=extra_field_id,
            value=i["answer"]
        )
        db.add(extra_field)

    await db.commit_rollback()
