from src.infrastructure.database import db, Institute, commit_rollback
from sqlalchemy import delete

async def delete_institute(institute_id: int):
    stmt = delete(Institute).where(Institute.id == institute_id)
    await db.execute(stmt)
    await commit_rollback()