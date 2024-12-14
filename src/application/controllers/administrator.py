from src.domain.services import administrator_service
from src.application.dto.admin import EditUserDTO
from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter, Body


router = APIRouter()


@router.get("/me", description="Return data about current user")
async def show_me(admin: CurrentAdmin):
    return await administrator_service.get_by_email(admin.username)


@router.get("/", description="Return all admins")
async def show_admins(admin: CurrentAdmin):
    return await administrator_service.show_administrators()


@router.patch("/{admin_id}", description="Edit an existing user")
async def edit_admin(
    admin: CurrentAdmin, admin_id: int, dto: EditUserDTO = Body(...)
):
    return await administrator_service.edit_administrator(admin_id, dto)
    

@router.delete("/{admin_id}", description="Delete an existing user")
async def delete_admin(admin: CurrentAdmin, admin_id: int):
    return await administrator_service.delete_administrator(admin_id)


@router.get("/universityRating", description="Return overall rating")
async def show_university_rating(admin: CurrentAdmin):
    return "University's rating is shown"


@router.get("/disciplineRating", description="Return discipline rating")
async def show_discipline_rating(admin: CurrentAdmin):
    return "Discipline's rating is shown"


@router.get("/teacherRating", description="Return teacher rating")
async def show_teacher_rating(admin: CurrentAdmin):
    return "Teacher's rating is shown"


@router.get("/reviews", description="Return all reviews")
async def show_reviews(admin: CurrentAdmin):
    return "Reviews are shown"


@router.get("/reviews/{review_id}", description="Return certain review")
async def show_review(admin: CurrentAdmin, review_id: int):
    return "Review is shown"


@router.get("/reviews/get_xlsx", description="Return .xlsx file with reviews")
async def get_xlsx_file_with_reviews(admin: CurrentAdmin):
    return ".xlsx file is given"


@router.patch("/lesson/{lesson_id}", description="Edit an existing lesson")
async def edit_lesson(admin: CurrentAdmin, lesson_id: int):
    return "Lesson is edited"
