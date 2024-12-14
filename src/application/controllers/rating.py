from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter


router = APIRouter()


@router.get("/university", description="Return overall rating")
async def show_university_rating(admin: CurrentAdmin):
    return "University's rating is shown"


@router.get("/discipline", description="Return discipline rating")
async def show_discipline_rating(admin: CurrentAdmin):
    return "Discipline's rating is shown"


@router.get("/teacher", description="Return teacher rating")
async def show_teacher_rating(admin: CurrentAdmin):
    return "Teacher's rating is shown"