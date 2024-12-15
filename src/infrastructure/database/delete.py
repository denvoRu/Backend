from sqlalchemy import delete
from src.infrastructure.database import db, commit_rollback


async def delete_from_instance_by_id(instance, instance_id: int):
    stmt = delete(instance).where(instance.id == instance_id)
    await db.execute(stmt)
    await commit_rollback()