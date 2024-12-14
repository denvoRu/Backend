from src.infrastructure.database.models.teacher import Teacher
from src.infrastructure.database.models.administrator import Administrator
from src.application.dto.shared import EditUserDTO
from src.infrastructure.database.initialize_database import get_session

from sqlalchemy import update


async def edit_user(user_id, dto: EditUserDTO, instance):
    data = dto.model_dump(exclude_none=True)
    async_session = get_session()
    
    async with async_session() as session:
        stmt = (update(instance)
            .where(instance.id == user_id)
            .values(**data)
        )
        
        await session.execute(stmt)
        await session.commit()
        

async def edit_admin(admin_id: int, dto: EditUserDTO):
    return await edit_user(admin_id, dto, Administrator)

async def edit_teacher(teacher_id: int, dto: EditUserDTO):
    return await edit_user(teacher_id, dto, Teacher)