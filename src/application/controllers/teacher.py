from src.infrastructure.enums.privilege import Privilege
from src.application.dto.shared import EditUserDTO
from src.domain.services import teacher_service, study_group_service
from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin

from fastapi import APIRouter, Body, Query
from typing import List
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
    institute_ids: str = Query(None, alias="institute_ids"),
    subject_ids: str = Query(None, alias="subject_ids"),
    not_in_subject_by_id: UUID4 = Query(None, alias="not_in_subject_by_id"),
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
        institute_ids,
        subject_ids,
        not_in_subject_by_id
    )


@router.get("/me", description="Show me")
async def get_me(teacher: CurrentTeacher):
    return await teacher_service.get_by_id(teacher, teacher.id)


@router.get("/me/subject", description="Show my subjects")
async def get_subject_of_me(
    teacher: CurrentTeacher,
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search")
):
    return await teacher_service.get_subjects(
        teacher.id,
        page,
        limit,
        desc,
        columns,
        sort,
        search
    )



@router.get("/{teacher_id}", description="Show teacher data (for admins)")
async def get_current_teacher(admin: CurrentAdmin, teacher_id: UUID4):
    return await teacher_service.get_by_id(admin, teacher_id)


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
    return await teacher_service.privilege.get_all(teacher_id)


@router.post("/{teacher_id}/privilege/{privilege}", description="Add teacher privilege (for admins)", status_code=201)
async def add_teacher_privilege(
    admin: CurrentAdmin, teacher_id: UUID4, privilege: Privilege
):
    return await teacher_service.privilege.add(teacher_id, privilege)


@router.delete("/{teacher_id}/privilege/{privilege}", description="Delete teacher privilege (for admins)")
async def delete_teacher_privilege(
    admin: CurrentAdmin, teacher_id: UUID4, privilege: Privilege
):
    return await teacher_service.privilege.delete(teacher_id, privilege)


@router.post("/{teacher_id}/subjects/", description="Add subjects to teacher (for admins)")
async def add_subjects_to_teacher(
    admin: CurrentAdmin, 
    teacher_id: UUID4, 
    subject_ids: List[UUID4] = Body(...)
):
    return await study_group_service.add_by_subject_ids(teacher_id, subject_ids)


@router.delete("/{teacher_id}/subjects/", description="Delete teacher subjects by id (for admins)")
async def delete_subjects_from_teacher(
    admin: CurrentAdmin, 
    teacher_id: UUID4, 
    subject_ids: List[UUID4]
):
    return await study_group_service.delete_many(teacher_id, subject_ids)
