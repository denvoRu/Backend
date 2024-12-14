from src.application.dto.admin.edit_user_dto import EditUserDTO
from src.infrastructure.repositories import (
    administrator_repository, teacher_repository
)


async def show_teachers():
    return await teacher_repository.all()

async def get_by_id(teacher_email: str):
    return await teacher_repository.get_by_id(teacher_email)

async def get_by_email(teacher_email: str):
    return await teacher_repository.get_by_email(teacher_email)

async def edit_teacher(admin_id: int, dto: EditUserDTO):
    await administrator_repository.edit_teacher(admin_id, dto)
    return { "status": "ok" }