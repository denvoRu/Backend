from src.domain.services import university_service
from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter


router = APIRouter()


@router.get("/rating", description="Show overall rating")
async def get_university_rating(admin: CurrentAdmin):
    return await university_service.get()
