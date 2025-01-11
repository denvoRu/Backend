from src.infrastructure.database import (
    Feedback, delete_from_instance_by_id
)

from uuid import UUID


async def delete_by_id(feedback_id: UUID):
    return await delete_from_instance_by_id(Feedback, feedback_id)