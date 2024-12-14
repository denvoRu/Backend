from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter

router = APIRouter()


@router.get("/{lesson_id}/reviews", description="Return all reviews")
async def show_reviews(admin: CurrentAdmin):
    return "Reviews are shown"

@router.post("/{lesson_id}/reviews", description="Send a new review")
async def add_review():
    return "Reviews are shown"

@router.get("/{lesson_id}/reviews/get_xlsx", description="Return .xlsx file with reviews")
async def get_xlsx_file_with_reviews(admin: CurrentAdmin):
    return ".xlsx file is given"
