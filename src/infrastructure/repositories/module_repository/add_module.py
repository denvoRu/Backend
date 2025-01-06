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
    for name in names:
        module = Module(
            institute_id=institute_id,
            name=name,
            rating=0            
        )
        db.add(module)
    
    await db.commit_rollback()
    