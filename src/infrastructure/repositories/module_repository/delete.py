from src.infrastructure.database import delete, Module
from typing import List


async def delete_by_id(module_id: int) -> None:
    await delete.delete_from_instance_by_id(Module, module_id)