from fastapi import FastAPI, APIRouter
import uvicorn

app = FastAPI()
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


@router.post("/createLesson", description="Create a new lesson as a teacher")
async def create_lesson():
    return "New lesson is added"


@router.post("/editLesson", description="Edit an existing lesson as an teacher")
async def edit_lesson():
    return "Current lesson is edited"


@router.post("/createQR", description="Create a new QR for a lesson")
async def create_qr():
    return "QR for current lesson is created"


@router.post("/editQR", description="Edit QR info for a lesson")
async def edit_lesson():
    return "Current QR is edited"


@router.get("/showStudentsThatVoted", description="Get students that voted")
async def edit_lesson():
    return "Students are shown"


@router.post("/showLessonsList", description="Get lessons list")
async def edit_lesson():
    return "Lessons list is shown"


app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
