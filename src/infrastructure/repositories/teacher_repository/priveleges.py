from src.infrastructure.database import (
    db, Privileges, commit_rollback
)
from sqlalchemy import delete, select


async def get_privileges(teacher_id: int):

    s = await db.execute(
        select(Privileges.privilage)
        .where(Privileges.teacher_id == teacher_id)
    )
    return s.all()
    
async def add_privilege(teacher_id: int, privilege: str):
    db.add(Privileges(teacher_id=teacher_id, privilage=privilege))
    await commit_rollback()

async def has_privilege(teacher_id: int, privilege: str):
    s = await db.execute(
        select(Privileges.id)
        .where(Privileges.privilage == privilege,
               Privileges.teacher_id == teacher_id)
    )
    
    return len(s.all()) > 0
    
async def delete_privilege(teacher_id: int, privilege: str):
    stmt = (delete(Privileges)
            .where(Privileges.teacher_id == teacher_id, 
                   Privileges.privilage == privilege))
    
    await db.execute(stmt)
    await commit_rollback()