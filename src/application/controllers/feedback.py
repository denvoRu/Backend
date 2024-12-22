from src.domain.extensions.check_role import CurrentUser
from src.application.dto.feedback import AddFeedbackDTO

from fastapi import APIRouter, Body


router = APIRouter()


@router.get("/{lesson_id}/feedback", description="Show all feedbacks")
async def get_feedbacks_of_lesson(admin: CurrentUser, lesson_id: int):
    return "Reviews are shown"


@router.get("/{lesson_id}/feedback/xlsx", description="Show .xlsx file with reviews")
async def get_xlsx_file_with_feedbacks(admin: CurrentUser, lesson_id: int):
    return ".xlsx file is given"


@router.post("/{lesson_id}/feedback", description="Send a new review", status_code=201)
async def add_feedback_to_lesson(lesson_id: int, dto: AddFeedbackDTO = Body(...)):
    return "Reviews are shown"
