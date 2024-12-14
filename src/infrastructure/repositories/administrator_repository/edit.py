from src.infrastructure.database.models.teacher import Teacher
from src.infrastructure.database.models.administrator import Administrator
from src.application.dto.shared import EditUserDTO
from src.infrastructure.database import db, commit_rollback

from sqlalchemy import update


async def edit_user(user_id, dto: EditUserDTO, instance):
    data = dto.model_dump(exclude_none=True)
    stmt = (update(instance)
        .where(instance.id == user_id)
        .values(**data)
    )
    
    await db.execute(stmt)
    await commit_rollback()
    

async def edit_admin(admin_id: int, dto: EditUserDTO):
    return await edit_user(admin_id, dto, Administrator)

async def edit_teacher(teacher_id: int, dto: EditUserDTO):
    return await edit_user(teacher_id, dto, Teacher)