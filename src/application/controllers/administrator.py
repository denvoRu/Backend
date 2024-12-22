from src.domain.services import administrator_service
from src.application.dto.shared import EditUserDTO
from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter, Body, Query


router = APIRouter()


@router.get("/me", description="Show data about current user")
async def get_me(admin: CurrentAdmin):
    return await administrator_service.get_by_id(admin.user_id)


@router.get("/", description="Show all admins")
async def get_all_admins(
    admin: CurrentAdmin, 
    page: int = 1,
    limit: int = 10,
    desc: int = 0,
    columns: str = Query(None, alias="columns"),
    sort: str = Query(None, alias="sort"),
    search: str = Query(None, alias="search"),
):
    return await administrator_service.get_administrators(
        page, 
        limit, 
        columns, 
        sort, 
        search,
        desc
    )


@router.patch("/{admin_id}", description="Edit an existing user")
async def edit_admin(
    admin: CurrentAdmin, admin_id: int, dto: EditUserDTO = Body(...)
):
    return await administrator_service.edit_administrator(admin_id, dto)
    

@router.delete("/{admin_id}", description="Delete an existing user")
async def delete_admin(admin: CurrentAdmin, admin_id: int):
    return await administrator_service.delete_administrator(admin_id)
