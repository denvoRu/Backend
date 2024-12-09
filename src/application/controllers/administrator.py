from fastapi import APIRouter

router = APIRouter()


@router.post("/user", description="Create a new user as an administrator")
async def create_user():
    return "User is created"


@router.patch("/user", description="Edit an existing user as an administrator")
async def edit_user():
    return "User's info is updated"


@router.get("/universityRating", description="Return overall rating")
async def show_university_rating():
    return "University's rating is shown"


@router.get("/disciplineRating", description="Return discipline rating")
async def show_discipline_rating():
    return "Discipline's rating is shown"


@router.get("/teacherRating", description="Return teacher rating")
async def show_teacher_rating():
    return "Teacher's rating is shown"


@router.get("/reviews", description="Return all reviews")
async def show_reviews():
    return "Reviews are shown"


@router.get("/reviews/:review_id", description="Return certain review")
async def show_review(review_id):
    return "Review is shown"


@router.get("/reviews/get_xlsx", description="Return .xlsx file with reviews")
async def get_xlsx_file_with_reviews():
    return ".xlsx file is given"


@router.patch("/lesson/:lesson_id", description="Edit an existing lesson")
async def edit_lesson():
    return "Lesson is edited"
