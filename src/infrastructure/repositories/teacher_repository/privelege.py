from src.infrastructure.database import Privilege, has_instance, add_instance, db

from sqlalchemy import delete, select
from uuid import UUID


async def get_by_id(teacher_id: UUID):
    """
    Gets teacher's privileges
    """
    s = await db.execute(
        select(Privilege.name)
        .where(Privilege.teacher_id == teacher_id)
    )
    return s.scalars().all()


async def add(teacher_id: UUID, name: str):
    """
    Adds a privilege to the teacher's privileges'
    """
    p = Privilege(teacher_id=teacher_id, name=name)
    await add_instance(p)


async def has_by_name(teacher_id: UUID, name: str):
    """
    Checks that teacher has a privilege with the given name
    """
    return await has_instance(
        Privilege, 
        (Privilege.teacher_id == teacher_id, 
         Privilege.name == name)
    )
    

async def delete_by_name(teacher_id: UUID, name: str):
    """
    Delete a privilege from the teacher's privileges by the given name'
    """
    stmt = (delete(Privilege)
            .where(Privilege.teacher_id == teacher_id, 
                   Privilege.name == name))
    
    await db.execute(stmt)
    await db.commit_rollback()
