from src.infrastructure.database import (
    Privileges, commit_rollback, 
    has_instance, add_instance, db
)

from sqlalchemy import delete, select
from uuid import UUID


async def get_privileges(teacher_id: UUID):
    s = await db.execute(
        select(Privileges.privilege)
        .where(Privileges.teacher_id == teacher_id)
    )
    return s.scalars().all()


async def add_privilege(teacher_id: UUID, privilege: str):
    p = Privileges(teacher_id=teacher_id, privilage=privilege)
    await add_instance(p)


async def has_privilege(teacher_id: UUID, privilege: str):
    return await has_instance(
        Privileges, 
        (Privileges.teacher_id == teacher_id,
        Privileges.privilege == privilege)
    )
    

async def delete_privilege(teacher_id: UUID, privilege: str):
    stmt = (delete(Privileges)
            .where(Privileges.teacher_id == teacher_id, 
                   Privileges.privilege == privilege))
    
    await db.execute(stmt)
    await commit_rollback()
