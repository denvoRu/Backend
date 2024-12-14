from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import administrator_repository


async def get_by_id(admin_id: str):
    return await administrator_repository.get_by_id(admin_id)

async def show_administrators(page, limit, columns, sort, filter): 
    return await administrator_repository.all(page, limit, columns, sort, filter)

async def edit_administrator(admin_id: int, dto: EditUserDTO):
    await administrator_repository.edit_admin(admin_id, dto)
    return { "status": "ok" }

async def delete_administrator(admin_id: str):
    await administrator_repository.delete_admin(admin_id)
    return { "status": "ok" }