from src.infrastructure.database import db

from sqlalchemy import delete, update


async def delete_from_instance_by_id(instance, instance_id: int):
    if hasattr(instance, "is_disabled"):
        return await save_delete_from_instance_by_id(
            instance, 
            instance_id
        )
    
    stmt = delete(instance).where(instance.id == instance_id)
    await db.execute(stmt)
    await db.commit_rollback()

async def save_delete_from_instance_by_id(instance, instance_id: int):
    stmt = update(instance)\
        .where(instance.id == instance_id)\
        .values(is_disabled=True)
    
    await db.execute(stmt)
    await db.commit_rollback()
