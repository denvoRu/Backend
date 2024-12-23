from src.infrastructure.database import Subject, delete_from_instance_by_id

from uuid import UUID


async def delete_by_id(subject_id: UUID) -> None:
    await delete_from_instance_by_id(Subject, subject_id)
