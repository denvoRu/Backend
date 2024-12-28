from src.infrastructure.database import Subject, has_instance, db

from uuid import UUID
from sqlalchemy import select, func
from typing import List


async def has_by_id(subject_id: UUID):
    return await has_instance(Subject, Subject.id == subject_id)


async def has_by_name(name: int):
    return await has_instance(Subject, Subject.name == name)


async def has_many(subject_ids: List[UUID]):
    stmt = select(func.count(Subject.id) == len(subject_ids))\
        .where(Subject.id.in_(subject_ids))
    
    result = await db.execute(stmt)
    
    return result.one()[0]