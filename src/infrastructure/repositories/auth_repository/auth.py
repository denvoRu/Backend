from src.infrastructure.database import (
    Administrator, Teacher, commit_rollback, db
)
from typing import TypeVar
from sqlalchemy import select


T = TypeVar("T")


async def __get_hashed_password_by_email(table: T, email: str) -> T:
    where_args = [table.email == email]

    if hasattr(table, "is_disabled"):
        where_args.append(table.is_disabled == False)

    s = select(table.id, table.password).where(*where_args)

    scalar = await db.execute(s)
    return scalar.one()


async def is_in_table(table: T, email: str) -> bool:
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
    db.add(user)
    await commit_rollback()

    return user
