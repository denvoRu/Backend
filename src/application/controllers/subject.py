from src.application.dto.subject import CreateSubjectDTO, EditSubjectDTO
from src.domain.services import subject_service
from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter, Body, Query

router = APIRouter()

@router.get("/", description="Show all subjects (for admins)")
async def show_all_subject(
    admin: CurrentAdmin, 
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search"),
    rating_start: int = Query(-1, alias="rating_start"),
    rating_end: int = Query(-1, alias="rating_end"),
    teacher_ids: str = Query(None, alias="teacher_ids"),
):
    return await subject_service.get_all(
        page, 
        limit,
        columns,
        sort, 
        search,
        desc,
        rating_start,
        rating_end,
        teacher_ids
    )

@router.get("/{subject_id}", description="Show certain subject (for admins)")
async def show_subject(admin: CurrentAdmin, subject_id: int):
    subject_service.get_by_id(subject_id)

@router.post("/", description="Create a new subject (for admins)")
async def create_subject(
    teacher: CurrentAdmin, dto: CreateSubjectDTO = Body(...)
):
    await subject_service.create_subject(dto)

@router.patch("/{subject_id}", description="Edit an existing subject (for admins)")
async def edit_subject(admin: CurrentAdmin, dto: EditSubjectDTO = Body(...)):
    return await subject_service.edit_subject(dto)

@router.delete("/{subject_id}", description="Delete an existing subject (for admins)")
async def delete_subject(admin: CurrentAdmin, subject_id: int):
    return await subject_service.delete_subject(subject_id)
