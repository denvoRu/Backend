from src.application.dto.subject import AddSubjectDTO, EditSubjectDTO
from src.domain.services import subject_service, study_group_service
from src.domain.extensions.check_role import CurrentAdmin

from fastapi import APIRouter, Body, Query
from typing import List
from pydantic import UUID4


router = APIRouter()


@router.get("/", description="Show all subjects (for admins)")
async def get_all_subject(
    admin: CurrentAdmin, 
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search"),
    teacher_ids: str = Query(None, alias="teacher_ids"),
    module_id: UUID4 = Query(None, alias="module_id"),
    not_in_module_by_id: UUID4 = Query(None, alias="not_in_module_by_id"),
    subject_without_teacher_by_id: UUID4 = Query(None, alias="subject_without_teacher_by_id"),
    not_has_const_link_by_teacher_id: UUID4 = Query(None, alias="not_has_const_link_by_teacher_id"),
):
    return await subject_service.get_all(
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc, 
        teacher_ids, 
        module_id,
        not_in_module_by_id,
        subject_without_teacher_by_id,
        not_has_const_link_by_teacher_id
    )


@router.get("/{subject_id}", description="Show certain subject (for admins)")
async def get_current_subject(admin: CurrentAdmin, subject_id: UUID4):
    return await subject_service.get_by_id(subject_id)


@router.post("/", description="Add a new subject (for admins)", status_code=201)
async def add_subject(
    teacher: CurrentAdmin, dto: AddSubjectDTO = Body(...)
):
    return await subject_service.add(dto)


@router.patch("/{subject_id}", description="Edit an existing subject (for admins)")
async def edit_subject(admin: CurrentAdmin, subject_id: UUID4, dto: EditSubjectDTO = Body(...)):
    return await subject_service.edit(subject_id, dto)


@router.delete("/{subject_id}", description="Delete an existing subject (for admins)")
async def delete_subject(admin: CurrentAdmin, subject_id: UUID4):
    return await subject_service.delete(subject_id)


@router.get("/{subject_id}/teachers", description="Show all teachers (for admins)")
async def get_teachers_by_subject(
    admin: CurrentAdmin, 
    subject_id: UUID4, 
    page: int = 1, 
    limit: int = 10,
    desc: int = 0,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search"),
    not_has_const_link: int = Query(0, alias="not_has_const_link"),
):
    return await study_group_service.get_teachers(
        subject_id,
        page,
        limit,
        columns,
        sort,
        search,
        desc,
        not_has_const_link
    )


@router.post("/{subject_id}/teachers", description="Add teachers to subject (for admins)", status_code=201)
async def add_teachers_to_subject(admin: CurrentAdmin, subject_id: UUID4, teacher_ids: List[UUID4] = Body(...)):
    return await study_group_service.add_by_teacher_ids(subject_id, teacher_ids)


@router.post("/{subject_id}/teachers/{teacher_id}", description="Add teacher to subject (for admins)", status_code=201)
async def add_teacher_to_subject(admin: CurrentAdmin, subject_id: UUID4, teacher_id: UUID4):
    return await study_group_service.add_by_teacher_id(subject_id, teacher_id)


@router.delete("/{subject_id}/teachers/{teacher_id}", description="Delete teacher from subject (for admins)")
async def delete_teacher_from_subject(admin: CurrentAdmin, subject_id: UUID4, teacher_id: UUID4):
    return await study_group_service.delete_by_teacher(subject_id, teacher_id)
