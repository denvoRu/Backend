from fastapi import APIRouter

router = APIRouter()


@router.get("/lessons", description="Show all lessons")
async def show_lessons():
    return "Lessons are shown"


@router.get("/lessons/:lesson_id", description="Show certain lesson")
async def show_lesson():
    return "Lesson is shown"


@router.post("/lessons", description="Create a new lesson")
async def create_lesson():
    return "New lesson is added"


@router.patch("/lessons/:lesson_id", description="Update an existing lesson")
async def edit_lesson(lesson_id):
    return "Current lesson is edited"


@router.post("/qr", description="Create a new QR for a lesson")
async def create_qr():
    return "QR for current lesson is created"


@router.patch("/qr/:qr_id", description="Update QR info for a lesson")
async def edit_qr(qr_id):
    return "Current QR is edited"


@router.get("/lesson/:lesson_id/reviews", description="Get students that added reviews for a certain lesson")
async def show_students(lesson_id):
    return "List of students is given"
