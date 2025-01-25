from src.domain.services import administrator_service
from src.application.dto.shared import EditUserDTO
from src.domain.extensions.check_role import CurrentAdmin

from fastapi import APIRouter, Body, Query
from pydantic import UUID4


router = APIRouter()  # creating an administrator's router


@router.get("/me", description="Show data about current user")
async def get_me(admin: CurrentAdmin):
    """
    Returns current administrator
    :param admin: user with admin role
    :return: current administrator
    """
    return await administrator_service.get_by_id(admin.id)


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
    """
    Returns all administrators
    :param admin: user with admin role
    :param page: current page number
    :param limit: limit of admins on the page
    :param desc: descending/ascending
    :param columns: params to show
    :param sort: params to sort
    :param search: search string
    :return: all administrators
    """
    return await administrator_service.get_all(
        page, 
        limit, 
        columns, 
        sort, 
        search, 
        desc
    )


@router.patch("/{admin_id}", description="Edit an existing user")
async def edit_admin(
    admin: CurrentAdmin, admin_id: UUID4, dto: EditUserDTO = Body(...)
):
    # edits admin with needed params
    return await administrator_service.edit(admin_id, dto) 
    

@router.delete("/{admin_id}", description="Delete an existing user")
async def delete_admin(admin: CurrentAdmin, admin_id: UUID4):
    return await administrator_service.delete(admin_id)
