from fastapi import APIRouter


router = APIRouter()

@router.post("/user", description="Create a new user as an administrator")
async def create_user():
    return "User is created"


@router.patch("/user", description="Edit an existing user as an administrator")
async def edit_user():
    return "User info is updated"


@router.get("/universityRating", description="Return overall rating")
async def show_university_rating():
    return "University rating is shown"


@router.get("/lessonRating", description="Return lesson rating")
async def show_lesson_rating():
    return "Lesson rating is shown"
