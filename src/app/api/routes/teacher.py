from fastapi import APIRouter, Depends, Response

router = APIRouter()


@router.post("/createLesson", description="Create a new lesson as a teacher")
async def create_lesson():
    return "New lesson is added"


@router.post("/editLesson", description="Edit an existing lesson as a teacher")
async def edit_lesson():
    return "Current lesson is edited"


@router.post("/createQR", description="Create a new QR for a lesson")
async def create_qr():
    return "QR for current lesson is created"


@router.post("/editQR", description="Edit QR info for a lesson")
async def edit_lesson():
    return "Current QR is edited"
