from src.domain.extensions.check_role import CurrentUser

from fastapi import APIRouter, Body, Query
from pydantic import UUID4


router = APIRouter()


@router.get("/const_link", description="Showa all const link (for admins)")
async def get_const_link(
    current_user: CurrentUser
): pass