from src.domain.enums.role import Role
from src.application.dto.admin.edit_user_dto import EditUserDTO
from src.infrastructure.repositories import administrator_repository


async def get_me(admin_email: str):
    return await administrator_repository.get_by_email(admin_email)

async def show_administrators(): 
    return await administrator_repository.all()

async def edit_administrator(admin_id: int, dto: EditUserDTO):
    return await administrator_repository.edit_admin(admin_id, dto)

async def edit_teacher(admin_id: int, dto: EditUserDTO):
    return await administrator_repository.edit_teacher(admin_id, dto)