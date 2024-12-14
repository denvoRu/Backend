from typing import List, TypeVar
from src.infrastructure.database.initialize_database import get_session
from sqlalchemy import select


TableInstance = TypeVar("TableInstance")

async def get_by_email(email: str, instance: TableInstance) -> TableInstance:
    async_session = get_session()

    async with async_session() as session:
        select(instance).where(instance.email == email)
        s = await session.execute(select(instance).where(instance.email == email))
        
        data: TableInstance = s.first()[0]
        return data
    
async def get_all(instance: TableInstance) -> List[TableInstance]:
    data: List[TableInstance] = []
    async_session = get_session()

    async with async_session() as session:
        s = await session.execute(select(instance))
        for i in s.all():
            print(i)
            data.append(i[0])
    
    return data
    