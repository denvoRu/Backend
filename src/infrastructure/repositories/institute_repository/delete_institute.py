from src.infrastructure.database import Institute, delete_from_instance_by_id

from uuid import UUID


async def delete_by_id(institute_id: UUID):
    await delete_from_instance_by_id(Institute, institute_id,)
