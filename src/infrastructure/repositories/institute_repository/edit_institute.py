from src.infrastructure.database import Institute, update_instance


async def update_by_id(institute_id: int, data: dict):
    await update_instance(Institute, institute_id, data)
