from src.infrastructure.database import Module, add_instance, db

from typing import List
from uuid import UUID


async def add(institute_id: UUID, name: str):
    module = Module(
        institute_id=institute_id,
        name=name,
        rating=0
    )
    await add_instance(module)


async def add_from_list(institute_id: UUID, names: List[str]):
    modules = []
    for name in names:
        modules.append(
                Module(
                institute_id=institute_id,
                name=name,
                rating=0            
            )
        )
    
    await add_instance(*modules)
    