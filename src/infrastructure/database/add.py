from src.infrastructure.database import db, commit_rollback


async def add_instance(instance):
    db.add(instance)
    await commit_rollback()