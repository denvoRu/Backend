from src.infrastructure.database import Institute, update

async def edit_institute(institute_id: int, data: dict):
    await update.update_instance(Institute, institute_id, data)