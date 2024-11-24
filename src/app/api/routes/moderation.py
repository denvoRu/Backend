from fastapi import APIRouter, Depends, Response

router = APIRouter()


@router.post("/createUser", description="Create a new user as an administrator")
async def create_user():
    return "User is created"


@router.post("/editUser", description="Edit an existing user as an administrator")
async def edit_user():
    return "User info is updated"


@router.get("/showUniversityRating", description="Show overall rating")
async def show_university_rating():
    return "University rating is shown"


@router.get("/showLessonRating", description="Show lesson rating")
async def show_lesson_rating():
    return "Lesson rating is shown"
