from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter


router = APIRouter()


@router.get("/{form_id}/reviews", description="Return all reviews")
async def get_reviews(admin: CurrentAdmin):
    return "Reviews are shown"


@router.post("/{form_id}/reviews", description="Send a new review", status_code=201)
async def add_review():
    return "Reviews are shown"


@router.get("/{form_id}/reviews/get_xlsx", description="Return .xlsx file with reviews")
async def get_xlsx_file_with_reviews(admin: CurrentAdmin):
    return ".xlsx file is given"
