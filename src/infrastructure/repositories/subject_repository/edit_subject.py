from src.infrastructure.database import Subject, update_instance

async def update_by_id(subject_id: int, dto):
    await update_instance(Subject, subject_id, dto)
