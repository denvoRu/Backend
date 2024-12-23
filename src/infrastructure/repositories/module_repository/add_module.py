from src.infrastructure.database import Module, add_instance


async def add(institute_id: int, name: str):
    module = Module(
        institute_id=institute_id,
        name=name,
        rating=0
    )
    await add_instance(module)
