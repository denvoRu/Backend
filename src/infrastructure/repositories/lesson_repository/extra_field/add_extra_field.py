from src.infrastructure.database import ExtraFieldSetting, add_instance

from uuid import UUID


async def add(lesson_id: UUID, dto: dict):
    extra_field = ExtraFieldSetting(
        lesson_id=lesson_id,
        extra_field_name=dto["name"]
    )

    await add_instance(extra_field)