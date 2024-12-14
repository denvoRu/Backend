from src.domain.services import administrator_service
from src.application.dto.shared import EditUserDTO
from src.domain.extensions.check_role import CurrentAdmin
from fastapi import APIRouter, Body


router = APIRouter()


@router.get("/me", description="Return data about current user")
async def show_me(admin: CurrentAdmin):
    return await administrator_service.get_by_id(admin.id)


@router.get("/", description="Return all admins")
async def show_admins(admin: CurrentAdmin):
    return await administrator_service.show_administrators()


@router.patch("/{admin_id}", description="Edit an existing user")
async def edit_admin(
    admin: CurrentAdmin, admin_id: int, dto: EditUserDTO = Body(...)
):
    return await administrator_service.edit_administrator(admin_id, dto)
    

@router.delete("/{admin_id}", description="Delete an existing user")
async def delete_admin(admin: CurrentAdmin, admin_id: int):
    return await administrator_service.delete_administrator(admin_id)
