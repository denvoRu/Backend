from src.infrastructure.database import Module, has_instance, db

from aiomodeus.student_voice import Module as ModeusModule
from typing import List
from uuid import UUID

"""
Methods that check module existence by some parameters
"""


async def has_by_id(module_id: UUID):
    return await has_instance(Module, Module.id == module_id)


async def has_by_name(name: int):
    return await has_instance(Module, Module.name == name)


async def not_has_from_modeus(
        institute_id: UUID,
        modules: List[ModeusModule]
) -> List[ModeusModule]:
    result = []

    for m in modules:
        item = await m.find_in_orm(
            db,
            Module,
            whereclause=(
                Module.is_disabled == False,
                Module.institute_id == institute_id,
                Module.name == m.name
            )
        )
        if len(item) == 0:
            result.append(m)

    return result
