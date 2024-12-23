from src.infrastructure.database import Subject, update_instance

from uuid import UUID


async def update_by_id(subject_id: UUID, dto):
    await update_instance(Subject, subject_id, dto)
