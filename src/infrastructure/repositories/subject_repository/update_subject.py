from src.infrastructure.database import update, Subject

async def update_by_id(subject_id: int, dto):
    await update.update_instance(Subject, subject_id, dto)