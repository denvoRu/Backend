from fastapi import APIRouter

router = APIRouter()

@router.get("/lessons", description="Show all lessons as a teacher")
async def show_lessons():
    return "Lessons are shown"

@router.post("/lesson", description="Create a new lesson as a teacher")
async def create_lesson():
    return "New lesson is added"


@router.patch("/lesson", description="Update an existing lesson as a teacher")
async def edit_lesson():
    return "Current lesson is edited"


@router.post("/qr", description="Create a new QR for a lesson")
async def create_qr():
    return "QR for current lesson is created"


@router.patch("/qr", description="Update QR info for a lesson")
async def edit_lesson():
    return "Current QR is edited"
