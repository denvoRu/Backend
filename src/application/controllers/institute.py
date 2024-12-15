from src.application.dto.institute import CreateInstitudeDTO, EditInstitudeDTO
from src.domain.services import institute_service
from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter, Body, Query

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
    return await institute_service.get_all(page, limit, columns, sort, search, desc)


@router.get("/{institute_id}", description="Get an existing institute with id")
async def get_current_institute(current_user: CurrentAdmin, institute_id: int):
    return await institute_service.get_by_id(institute_id)


@router.post("/", description="Create a new institute")
async def create_institute(
    current_user: CurrentAdmin, dto: CreateInstitudeDTO = Body(...)
):
    return await institute_service.create_institute(dto)


@router.patch("/{institute_id}", description="Edit an existing institute")
async def edit_institute(
    current_user: CurrentAdmin, institute_id: int, dto: EditInstitudeDTO = Body(...)
):
    return await institute_service.edit_institute(institute_id, dto)


@router.delete("/{institute_id}", description="Delete an existing institute")
async def delete_institute(current_user: CurrentAdmin, institute_id: int):
    return await institute_service.delete_institute(institute_id)
