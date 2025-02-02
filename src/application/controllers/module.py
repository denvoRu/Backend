from src.application.dto.module import AddModuleDTO, EditModuleDTO
from src.domain.services import module_service
from src.domain.extensions.check_role import CurrentAdmin

from fastapi import APIRouter, Body, Query
from pydantic import UUID4


router = APIRouter()


@router.get("/", description="Get all existing modules (for admins)")
async def get_all_modules(
    current_user: CurrentAdmin,
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    institute_id: UUID4 = Query(None, alias="institute_id"),
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search"),    
):
    return await module_service.get_all(
        page, limit, columns, sort, search, desc, institute_id
    )


@router.get("/subjects", description="Get all existing modules and their subjects (for admins)")
async def get_all_modules_with_subjects(
    current_user: CurrentAdmin,
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search"),
    rating_start: int = Query(-1, alias="rating_start"),
    rating_end: int = Query(-1, alias="rating_end"),
    institute_ids: str = Query(None, alias="institute_ids"),
    teacher_ids: str = Query(None, alias="teacher_ids"),
):
    return await module_service.get_all_with_subjects(
        page, 
        limit, 
        sort, 
        search, 
        desc, 
        rating_start,
        rating_end, 
        institute_ids,
        teacher_ids
    )


@router.get("/{module_id}", description="Get an existing module with id (for admins)")
async def get_current_module(current_user: CurrentAdmin, module_id: UUID4):
    return await module_service.get_by_id(module_id)


@router.post("/", description="Add a new module", status_code=201)
async def add_module(
    current_user: CurrentAdmin, 
    dto: AddModuleDTO = Body(...)
):
    return await module_service.add(dto)


@router.patch("/{module_id}", description="Edit an existing module (for admins)")
async def edit_module(
    current_user: CurrentAdmin, 
    module_id: UUID4, 
    dto: EditModuleDTO = Body(...)
):
    return await module_service.edit(module_id, dto)


@router.delete("/{module_id}", description="Delete an existing module (for admins)")
async def delete_module(current_user: CurrentAdmin, module_id: UUID4):
    return await module_service.delete(module_id)
