from src.infrastructure.database import Subject, add as add_instance

async def add(institute_id: int, module_id: int, name: str):
    module = Subject(
        institute_id=institute_id,
        module_id=module_id,
        name=name,
        rating=0
    )
    await add_instance(module)
   