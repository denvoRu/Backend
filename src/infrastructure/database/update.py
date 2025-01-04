from src.infrastructure.database import db
from sqlalchemy import update


async def update_instance(instance, instance_id: int, data: dict):
    where_args = [instance.id == instance_id]

    if hasattr(instance, "is_disabled"):
        where_args.append(instance.is_disabled == False)

    stmt = update(instance).where(*where_args).values(**data)
    await db.execute(stmt)
    await db.commit_rollback()
