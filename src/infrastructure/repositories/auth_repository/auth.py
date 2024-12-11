from typing import TypeVar
from infrastructure.database.models.administrator import Administrator
from infrastructure.database.models.teacher import Teacher
from sqlalchemy.orm import Session
from sqlalchemy import select

T = TypeVar("T")

def __get_hashed_password_by_email(table: T, email: str) -> T:
    s = select(getattr(table, "password")).where(getattr(table, "email") == email)
    return Session.scalars(s).one()

def is_in_table(table: T, email: str) -> bool:
    s = select(getattr(table, "email")).where(getattr(table, "email") == email)
    return Session.scalars(s).one() is not None


def get_teacher_password_by_email(email: str):
    return __get_hashed_password_by_email(Teacher, email)

def get_admin_password_by_email(email: str):
    return __get_hashed_password_by_email(Administrator, email)


def add_user(user: T):
    Session.add(user)
    Session.commit()