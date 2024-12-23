from src.infrastructure.database import Institute, update_instance

from uuid import UUID


async def update_by_id(institute_id: UUID, data: dict):
    await update_instance(Institute, institute_id, data)
