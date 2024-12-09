from fastapi import APIRouter

router = APIRouter()


@router.get("/form/:form_id", description="Get an existing form with id")
async def get_form(form_id):
    return "Form is shown"


@router.patch("/form/:form_id", description="Edit an existing form with id")
async def edit_form(form_id):
    return "Form is updated"


@router.post("/form/:form_id", description="Create a form")
async def create_form():
    return "New form is created"
