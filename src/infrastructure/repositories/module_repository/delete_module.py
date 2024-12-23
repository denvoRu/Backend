from src.infrastructure.database import Module, delete_from_instance_by_id

from uuid import UUID


async def delete_by_id(module_id: UUID) -> None:
    await delete_from_instance_by_id(Module, module_id)
