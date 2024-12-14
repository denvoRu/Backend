from src.application.dto.shared import EditUserDTO
from src.infrastructure.repositories import (
    administrator_repository, teacher_repository
)


async def show_teachers():
    return await teacher_repository.all()

async def get_by_id(teacher_id: str):
    return await teacher_repository.get_by_id(teacher_id)

async def edit_teacher(admin_id: int, dto: EditUserDTO):
    await administrator_repository.edit_teacher(admin_id, dto)
    return { "status": "ok" }

async def delete_teacher(teacher_id: int):
    await teacher_repository.delete_teacher(teacher_id)
    return { "status": "ok" }