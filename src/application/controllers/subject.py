from src.application.dto.subject import CreateSubjectDTO, EditSubjectDTO
from src.domain.services import subject_service, study_group_service
from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter, Body, Query


router = APIRouter()


@router.get("/", description="Show all subjects (for admins)")
async def get_all_subject(
    admin: CurrentAdmin, 
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    module_id: int = Query(None, alias="module_id"),
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
        teacher_ids,
        module_id
    )


@router.get("/{subject_id}", description="Show certain subject (for admins)")
async def get_current_subject(admin: CurrentAdmin, subject_id: int):
    return await subject_service.get_by_id(subject_id)


@router.post("/", description="Create a new subject (for admins)", status_code=201)
async def create_subject(
    teacher: CurrentAdmin, dto: CreateSubjectDTO = Body(...)
):
    return await subject_service.create_subject(dto)


@router.patch("/{subject_id}", description="Edit an existing subject (for admins)")
async def edit_subject(admin: CurrentAdmin, dto: EditSubjectDTO = Body(...)):
    return await subject_service.edit_subject(dto)


@router.delete("/{subject_id}", description="Delete an existing subject (for admins)")
async def delete_subject(admin: CurrentAdmin, subject_id: int):
    return await subject_service.delete_subject(subject_id)


@router.get("/{subject_id}/teachers", description="Show all teachers (for admins)")
async def get_teachers_by_subject(
    admin: CurrentAdmin, 
    subject_id: int, 
    page: int = 1, 
    limit: int = 10,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search"),
    desc: int = 0
):
    return await study_group_service.get_teachers(
        subject_id,
        page,
        limit,
        columns,
        sort,
        search,
        desc
    )


@router.post("/{subject_id}/teachers/{teacher_id}", description="Add teacher to subject (for admins)", status_code=201)
async def add_teacher_to_subject(admin: CurrentAdmin, subject_id: int, teacher_id: int):
    return await study_group_service.add_teacher(subject_id, teacher_id)


@router.delete("/{subject_id}/teachers/{teacher_id}", description="Delete teacher from subject (for admins)")
async def delete_teacher_from_subject(admin: CurrentAdmin, subject_id: int, teacher_id: int):
    return await study_group_service.delete_teacher(subject_id, teacher_id)


@router.get("/{subject_id}/active", description="Show active lesson of subject if subject has infinity link")
async def get_active_lesson_of_subject(subject_id: int):
    # TODO check if subject has infinity link
    return # await subject_service.get_by_id(subject_id)
