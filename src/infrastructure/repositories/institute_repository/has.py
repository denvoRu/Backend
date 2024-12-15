from src.infrastructure.database import db, Institute

from sqlalchemy import select


async def has_institute(institude_name: str):
    s = await db.execute(
        select(Institute.id)
        .where(Institute.name == institude_name)
    )
    
    return len(s.all()) > 0

async def has_institute_by_id(institute_id: int):
    s = await db.execute(
        select(Institute.id)
        .where(Institute.id == institute_id)
    )
    
    return len(s.all()) > 0