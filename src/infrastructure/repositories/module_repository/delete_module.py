from src.infrastructure.database import delete_from_instance_by_id, Module

async def delete_by_id(module_id: int) -> None:
    await delete_from_instance_by_id(Module, module_id)