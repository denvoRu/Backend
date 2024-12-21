from src.infrastructure.database import db, commit_rollback
from sqlalchemy import update


async def update_instance(instance, instance_id: int, data: dict):
    stmt = update(instance).where(instance.id == instance_id).values(**data)
    await db.execute(stmt)
    await commit_rollback()
