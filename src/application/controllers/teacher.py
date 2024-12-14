from src.domain.services import teacher_service
from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin
from fastapi import APIRouter

router = APIRouter()


@router.get("/", description="Show all teachers")
async def show_teachers(admin: CurrentAdmin):
    return await teacher_service.show_teachers()


@router.get("/{teacher_id}", description="Show teacher data")
async def show_teacher(admin: CurrentAdmin):
    return await teacher_service.get_by_id(teacher_email)


@router.get("/lessons", description="Show all lessons")
async def show_lessons(teacher: CurrentTeacher):
    return "Lessons are shown"



@router.get("/lessons/{lesson_id}", description="Show certain lesson")
async def show_lesson(teacher: CurrentTeacher, lesson_id: int):
    return "Lesson is shown"


@router.post("/lessons", description="Create a new lesson")
async def create_lesson(teacher: CurrentTeacher):
    return "New lesson is added"


@router.patch("/lessons/{lesson_id}", description="Update an existing lesson")
async def edit_lesson(teacher: CurrentTeacher, lesson_id: int):
    return "Current lesson is edited"


@router.post("/qr", description="Create a new QR for a lesson")
async def create_qr(teacher: CurrentTeacher):
    return "QR for current lesson is created"


@router.patch("/qr/{qr_id}", description="Update QR info for a lesson")
async def edit_qr(teacher: CurrentTeacher, qr_id: int):
    return "Current QR is edited"


@router.get("/lesson/{lesson_id}/reviews", description="Get students that added reviews for a certain lesson")
async def show_students(teacher: CurrentTeacher, lesson_id: int):
    return "List of students is given"
