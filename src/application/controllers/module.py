from src.application.dto.module import CreateModuleDTO, EditModuleDTO
from src.domain.services import module_service
from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter, Body, Query

router = APIRouter()


@router.get("/", description="Get all existing modules")
async def get_all_modules(
    current_user: CurrentAdmin,
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    filter: str = Query(None, alias="filter"),
):
    return await module_service.get_all(page, limit, columns, sort, filter, desc)


@router.get("/{module_id}", description="Create a new module")
async def get_module(current_user: CurrentAdmin, module_id: int):
    return await module_service.get_by_id(module_id)



@router.post("/", description="Create a new module")
async def create_module(
    current_user: CurrentAdmin, dto: CreateModuleDTO = Body(...)
):
    return await module_service.create_module(dto)


@router.delete("/{module_id}", description="Delete an existing module")
async def delete_module(current_user: CurrentAdmin, module_id: int):
    return await module_service.delete_module(module_id)
