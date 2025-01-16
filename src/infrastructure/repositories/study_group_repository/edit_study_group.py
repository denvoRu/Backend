from src.infrastructure.database import StudyGroup, update_instance

from uuid import UUID


async def update_by_id(study_group_id: UUID, dto: dict):
    return await update_instance(StudyGroup, study_group_id, dto)
