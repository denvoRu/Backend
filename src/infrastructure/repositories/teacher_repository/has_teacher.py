from src.infrastructure.database import Teacher, has_instance

from typing import List
from sqlalchemy import select, func
from uuid import UUID


async def has_by_id(teacher_id: UUID) -> bool:
    return await has_instance(Teacher, Teacher.id == teacher_id)


async def has_many(teacher_ids: List[UUID]) -> bool:
    return all(
        [await has_by_id(teacher_id) for teacher_id in teacher_ids]
    )