from src.infrastructure.database import ExtraFieldSetting, delete_from_instance_by_id

from uuid import UUID


async def delete_by_id(extra_field_id: UUID):
    await delete_from_instance_by_id(
        ExtraFieldSetting,
        extra_field_id
    )