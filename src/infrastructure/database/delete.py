from sqlalchemy import delete
from src.infrastructure.database import db, commit_rollback


async def delete_user(admin_id: int, instance):
    stmt = delete(instance).where(instance.id == admin_id)
    await db.execute(stmt)
    await commit_rollback()