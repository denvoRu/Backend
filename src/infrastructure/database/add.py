from src.infrastructure.database import db, commit_rollback


async def add_instance(*instance):
    for item in instance:
        db.add(item)
    await commit_rollback()
    