from src.infrastructure.database import Subject, has_instance, db

from uuid import UUID
from aiomodeus.student_voice import Subject as SubjectModeus
from sqlalchemy import select, func
from typing import List

"""
Methods that check subject existence by some parameters
"""


async def has_by_id(subject_id: UUID):
    return await has_instance(Subject, Subject.id == subject_id)


async def has_by_name(name: int):
    return await has_instance(Subject, Subject.name == name)


async def has_many(subject_ids: List[UUID]):
    stmt = select(func.count(Subject.id) == len(subject_ids)).where(
        Subject.id.in_(subject_ids),
        Subject.is_disabled == False
    )

    result = await db.execute(stmt)

    return result.one()[0]


async def not_has_from_modeus(subjects: List[SubjectModeus]) -> List[SubjectModeus]:
    result = []

    for subject in subjects:
        item = await subject.find_in_orm(
            db,
            Subject,
            whereclause=(
                Subject.name == subject.name,
                Subject.is_disabled == False
            ),
            columns=["id"]
        )
        if len(item) == 0:
            result.append(subject)

    return result
