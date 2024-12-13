from src.infrastructure.database.initialize_database import get_session
from src.infrastructure.database.models.administrator import Administrator
from src.infrastructure.database.models.teacher import Teacher
from typing import TypeVar
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T")

async def __get_hashed_password_by_email(table: T, email: str) -> T:
    s = select(table.password).where(table.email == email)
    session_async = get_session()
    async with session_async() as session:
        scalar = await session.execute(s)
        return scalar.one()[0]

async def is_in_table(table: T, email: str) -> bool:
    s = select(table.email).where(table.email == email)
    session_async = get_session()
    async with session_async as session:
        return (await session.execute(s)).one_or_none() is not None


async def get_teacher_password_by_email(email: str):
    return await __get_hashed_password_by_email(Teacher, email)

async def get_admin_password_by_email(email: str):
    return await __get_hashed_password_by_email(Administrator, email)


async def add_user(user: T):
    s = get_session()
    async with s() as session:
        session.add(user)
        await session.commit()