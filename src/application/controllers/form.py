from src.domain.extensions.check_role import CurrentTeacher
from fastapi import APIRouter


router = APIRouter()


@router.get("/{form_id}", description="Get an existing form with id")
async def get_form(teacher: CurrentTeacher, form_id: int):
    return "Form is shown"


@router.patch("/{form_id}", description="Edit an existing form with id")
async def edit_form(teacher: CurrentTeacher, form_id: int):
    return "Form is updated"


@router.post("/{form_id}", description="Create a form")
async def create_form(teacher: CurrentTeacher, form_id: int):
    return "New form is created"
