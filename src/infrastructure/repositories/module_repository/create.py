from src.infrastructure.database import Module, db, commit_rollback


async def add(name: str):
    module = Module(
        name=name,
        rating=0
    )
    db.add(module)
    await commit_rollback()