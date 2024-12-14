from src.infrastructure.database import get_session, Privileges
from sqlalchemy import delete, select


async def get_privileges(teacher_id: int):
    async_session = get_session()
    async with async_session() as session:
        s = await session.execute(select(Privileges.privilage).where(Privileges.teacher_id == teacher_id))
        return s.all()
    
async def add_privilege(teacher_id: int, privilege: str):
    async_session = get_session()
    async with async_session() as session:
        session.add(Privileges(teacher_id=teacher_id, privilage=privilege))
        await session.commit()

async def has_privilege(teacher_id: int, privilege: str):
    async_session = get_session()
    async with async_session() as session:
        s = await session.execute(
            select(Privileges.id)
            .where(Privileges.privilage == privilege and Privileges.teacher_id == teacher_id)
        )
        
        return len(s.all()) > 0
    
async def delete_privilege(teacher_id: int, privilege: str):
    async_session = get_session()
    async with async_session() as session:
        stmt = (delete(Privileges)
                .where(Privileges.teacher_id == teacher_id, 
                       Privileges.privilage == privilege))
        
        await session.execute(stmt)
        await session.commit()