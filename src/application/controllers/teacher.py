from src.infrastructure.enums.privileges import Privileges
from src.application.dto.shared import EditUserDTO
from src.domain.services import teacher_service
from src.domain.extensions.check_role import CurrentTeacher, CurrentAdmin
from fastapi import APIRouter, Body

router = APIRouter()

@router.get("/me", description="Show me")
async def show_me(teacher: CurrentTeacher):
    return await teacher_service.get_by_id(teacher.id)


@router.get("/", description="Show all teachers (for admins)")
async def show_teachers(admin: CurrentAdmin):
    return await teacher_service.show_teachers()


@router.get("/{teacher_id}", description="Show teacher data (for admins)")
async def show_teacher(admin: CurrentAdmin, teacher_id: int):
    return await teacher_service.get_by_id(teacher_id)


@router.patch("/{teacher_id}", description="Edit a teacher (for admins)")
async def edit_teacher(
    admin: CurrentAdmin, teacher_id: int, dto: EditUserDTO = Body(...)
):
    return await teacher_service.edit_teacher(teacher_id, dto)


@router.delete("/{teacher_id}", description="Delete a teacher (for admins)")
async def delete_teacher(admin: CurrentAdmin, teacher_id: int):
    return await teacher_service.delete_teacher(teacher_id)

@router.get("/{teacher_id}/privilege", description="Get a teacher's privilege (for admins)")
async def get_teacher_privilege(admin: CurrentAdmin, teacher_id: int):
    return await teacher_service.get_privileges(teacher_id)

@router.post("/{teacher_id}/privilege/{privilege}", description="Add teacher privilege (for admins)")
async def get_teacher_privilege(
    admin: CurrentAdmin, teacher_id: int, privilege: Privileges
):
    return await teacher_service.add_privilege(teacher_id, privilege)

@router.delete("/{teacher_id}/privilege/{privilege}", description="Delete teacher privilege (for admins)")
async def get_teacher_privilege(
    admin: CurrentAdmin, teacher_id: int, privilege: Privileges
):
    return await teacher_service.delete_privilege(teacher_id, privilege)
