from src.infrastructure.database import delete_from_instance_by_id, Subject


async def delete_by_id(subject_id: int) -> None:
    await delete_from_instance_by_id(Subject, subject_id)