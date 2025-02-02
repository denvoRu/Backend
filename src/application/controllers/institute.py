from src.application.dto.institute import AddInstituteDTO, EditInstituteDTO
from src.domain.services import institute_service
from src.domain.extensions.check_role import CurrentAdmin

from fastapi import APIRouter, Body, Query
from pydantic import UUID4


router = APIRouter()


@router.get("/", description="Get all existing institutes")
async def get_all_institutes(
    current_user: CurrentAdmin,
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search"),
):
    return await institute_service.get_all(
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc
    )


@router.get("/{institute_id}", description="Get an existing institute with id")
async def get_current_institute(
    current_user: CurrentAdmin, 
    institute_id: UUID4
):
    return await institute_service.get_by_id(institute_id)


@router.post("/", description="Add a new institute", status_code=201)
async def add_institute(
    current_user: CurrentAdmin, 
    dto: AddInstituteDTO = Body(...)
):
    return await institute_service.add(dto)


@router.patch("/{institute_id}", description="Edit an existing institute")
async def edit_institute(
    current_user: CurrentAdmin, 
    institute_id: UUID4, 
    dto: EditInstituteDTO = Body(...)
):
    return await institute_service.edit(institute_id, dto)


@router.delete("/{institute_id}", description="Delete an existing institute")
async def delete_institute(
    current_user: CurrentAdmin, 
    institute_id: UUID4
):
    return await institute_service.delete(institute_id)
