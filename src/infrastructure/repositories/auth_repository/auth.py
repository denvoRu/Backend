from src.infrastructure.database import db, commit_rollback
from src.infrastructure.database.models.administrator import Administrator
from src.infrastructure.database.models.teacher import Teacher
from typing import TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T")

async def __get_hashed_password_by_email(table: T, email: str) -> T:
    s = select(table.id, table.password).where(table.email == email)

    scalar = await db.execute(s)
    return scalar.one()

async def is_in_table(table: T, email: str) -> bool:
    s = select(table.email).where(table.email == email)
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