from src.infrastructure.enums.privilege import Privilege
from src.application.dto.shared import EditUserDTO
from src.domain.services import teacher_service
from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin

from fastapi import APIRouter, Body, Query
from pydantic import UUID4

router = APIRouter()


@router.get("/", description="Show all teachers (for admins)")
async def get_all_teachers(
    admin: CurrentAdmin, 
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search"),
    rating_start: int = Query(-1, alias="rating_start"),
    rating_end: int = Query(-1, alias="rating_end"),
    subject_ids: str = Query(None, alias="subject_ids")
):
    return await teacher_service.get_all(
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc, 
        rating_start, 
        rating_end, 
        subject_ids
    )


@router.get("/me", description="Show me")
async def get_me(teacher: CurrentTeacher):
    return await teacher_service.get_by_id(teacher.user_id)


@router.get("/{teacher_id}", description="Show teacher data (for admins)")
async def get_current_teacher(admin: CurrentAdmin, teacher_id: UUID4):
    return await teacher_service.get_by_id(teacher_id)


@router.patch("/{teacher_id}", description="Edit a teacher (for admins)")
async def edit_teacher(
    admin: CurrentAdmin, teacher_id: UUID4, dto: EditUserDTO = Body(...)
):
    return await teacher_service.edit(teacher_id, dto)


@router.delete("/{teacher_id}", description="Delete a teacher (for admins)")
async def delete_teacher(admin: CurrentAdmin, teacher_id: UUID4):
    return await teacher_service.delete(teacher_id)

@router.get("/{teacher_id}/privilege", description="Get a teacher's privilege (for admins)")
async def get_teacher_privileges(admin: CurrentAdmin, teacher_id: UUID4):
    return await teacher_service.get_privileges(teacher_id)

@router.post("/{teacher_id}/privilege/{privilege}", description="Add teacher privilege (for admins)", status_code=201)
async def add_teacher_privilege(
    admin: CurrentAdmin, teacher_id: UUID4, privilege: Privilege
):
    return await teacher_service.add_privilege(teacher_id, privilege)

@router.delete("/{teacher_id}/privilege/{privilege}", description="Delete teacher privilege (for admins)")
async def delete_teacher_privilege(
    admin: CurrentAdmin, teacher_id: UUID4, privilege: Privilege
):
    return await teacher_service.delete_privilege(teacher_id, privilege)
