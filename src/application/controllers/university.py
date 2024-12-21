from src.domain.services import university_service
from fastapi import APIRouter


router = APIRouter()


@router.get("/rating", description="Return overall rating")
async def get_university_rating():
    return await university_service.get_rating()