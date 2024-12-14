from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter, Body

router = APIRouter()


@router.get("/", description="Return all reviews")
async def show_reviews(admin: CurrentAdmin):
    return "Reviews are shown"

@router.post("/", description="Send a new review")
async def add_review():
    return "Reviews are shown"

@router.get("/{review_id}", description="Return certain review")
async def show_review(admin: CurrentAdmin, review_id: int):
    return "Review is shown"


@router.get("/{review_id}/get_xlsx", description="Return .xlsx file with reviews")
async def get_xlsx_file_with_reviews(admin: CurrentAdmin):
    return ".xlsx file is given"
