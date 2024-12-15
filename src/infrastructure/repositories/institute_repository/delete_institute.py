from src.infrastructure.database import Institute, delete

async def delete_institute(institute_id: int):
    await delete.delete_from_instance_by_id(Institute, institute_id,)