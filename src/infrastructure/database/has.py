from src.infrastructure.database import db
from sqlalchemy import select

async def has_instance(instance, where):
    s = await db.execute(
        select(instance.id)
        .where(where)
    )
    
    return len(s.all()) > 0