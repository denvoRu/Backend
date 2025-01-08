from src.infrastructure.database import (
    Administrator, Teacher, db
)
from typing import TypeVar
from sqlalchemy import select


T = TypeVar("T")


async def __get_hashed_password_by_email(table: T, email: str) -> T:
    where_args = [table.email == email]

    if hasattr(table, "is_disabled"):
        where_args.append(table.is_disabled == False)

    s = select(table.id, table.password).where(*where_args)

    try: 
        scalar = await db.execute(s)
        return scalar.one()
    except Exception: 
        await db.commit_rollback()
        raise Exception("User not found")

async def is_in_table(table: T, email: str) -> bool:
    """
    Checks if some user is in the table (by email)
    """
    where_args = [table.email == email]

    if hasattr(table, "is_disabled"):
        where_args.append(table.is_disabled == False)

    s = select(table.email).where(*where_args)
    executed = await db.execute(s)
    return len(executed.all()) > 0


async def get_teacher_password_by_email(email: str):
    return await __get_hashed_password_by_email(Teacher, email)


async def get_admin_password_by_email(email: str):
    return await __get_hashed_password_by_email(Administrator, email)


async def add_user(user: T):
    """
    Adds a user to the database
    """
    db.add(user)
    await db.commit_rollback()

    return user
