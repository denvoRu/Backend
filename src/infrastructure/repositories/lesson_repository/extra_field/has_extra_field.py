from src.infrastructure.database import ExtraFieldSetting, has_instance

from uuid import UUID


async def has_by_id(extra_field_id: UUID):
    return await has_instance(
        ExtraFieldSetting, 
        ExtraFieldSetting.id == extra_field_id
    )


async def has_by_name(lesson_id: UUID, name: str):
    return await has_instance(
        ExtraFieldSetting, (
            ExtraFieldSetting.lesson_id == lesson_id, 
            ExtraFieldSetting.extra_field_name == name
        )
    )
