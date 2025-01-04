from src.infrastructure.database import db


async def add_instance(*instance):
    for item in instance:
        db.add(item)
    await db.commit_rollback()
    