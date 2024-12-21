from src.infrastructure.database import Module, add_instance


async def add(name: str):
    module = Module(
        name=name,
        rating=0
    )
    await add_instance(module)
