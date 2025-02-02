from src.application.dto.const_link import AddConstLinkDTO, EditConstLinkDTO
from src.domain.services import const_link_service
from src.domain.extensions.check_role import CurrentAdmin

from fastapi import APIRouter, Body, Query
from pydantic import UUID4


router = APIRouter()


@router.get("/", description="Show all const link (for admins)")
async def get_const_link(
    admin: CurrentAdmin,
    institute_id: UUID4,
    page: int = 1,
    limit: int = 10,
    search: str = Query(None, alias="search"),
): 
    return await const_link_service.get_all(
        institute_id,
        page, 
        limit, 
        search
    )


@router.get("/active/{const_link_id}", description="Show lesson data if this lesson is active for this const link")
async def get_data_of_active_lesson(const_link_id: UUID4):
    return await const_link_service.get_active(const_link_id)


@router.post("/", description="Add a new const link (for admins)", status_code=201)
async def add_const_link(
    admin: CurrentAdmin,
    dto: AddConstLinkDTO = Body(...), 
): 
    return await const_link_service.add(dto)


@router.patch("/{const_link_id}", description="Edit const link (for admins)")
async def edit_const_link(
    admin: CurrentAdmin,
    const_link_id: UUID4, 
    dto: EditConstLinkDTO = Body(...),
): 
    return await const_link_service.edit(const_link_id, dto)


@router.delete("/{const_link_id}", description="Delete const link (for admins)")
async def delete_const_link(
    admin: CurrentAdmin,
    const_link_id: UUID4, 
): 
    return await const_link_service.delete(const_link_id)