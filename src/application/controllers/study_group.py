from src.domain.services import study_group_service

from fastapi import APIRouter, Body
from datetime import date
from pydantic import UUID4


router = APIRouter()


@router.get("/active/{study_group_id}", description="Show lesson data if this lesson is active for this study group")
async def get_data_of_active_lesson(study_group_id: UUID4):
    return await study_group_service.get_active(study_group_id)