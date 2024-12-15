from src.infrastructure.database import db, Institute, commit_rollback
from sqlalchemy import update

async def edit_institute(institute_id: int, data: dict):
    stmt = update(Institute).where(Institute.id == institute_id).values(**data)
    await db.execute(stmt)
    await commit_rollback()