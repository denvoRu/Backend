from src.domain.extensions.check_role import CurrentUser
from src.domain.services import feedback_service
from src.application.dto.feedback import AddFeedbackDTO

from fastapi import APIRouter, Body
from pydantic import UUID4


router = APIRouter()


@router.get("/{lesson_id}/feedback", description="Show all feedbacks")
async def get_feedbacks_of_lesson(user: CurrentUser, lesson_id: UUID4):
    return await feedback_service.get_by_id(user, lesson_id)


@router.get("/{lesson_id}/feedback/xlsx", description="Show .xlsx file with reviews")
async def get_xlsx_file_with_feedbacks(user: CurrentUser, lesson_id: UUID4):
    return await feedback_service.get_xlsx_by_id(user, lesson_id)


@router.post("/{lesson_id}/feedback", description="Send a new review", status_code=201)
async def add_feedback_to_lesson(lesson_id: UUID4, dto: AddFeedbackDTO = Body(...)):
    return await feedback_service.add(lesson_id, dto)
