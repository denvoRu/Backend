from src.infrastructure.database import Subject, add_instance

from uuid import UUID


async def add(module_id: UUID, name: str):
    module = Subject(
        module_id=module_id,
        name=name,
        rating=0
    )
    await add_instance(module)
