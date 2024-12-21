from src.infrastructure.database import Institute, delete_from_instance_by_id


async def delete_by_id(institute_id: int):
    await delete_from_instance_by_id(Institute, institute_id,)
