from src.infrastructure.enums.role import Role
from src.infrastructure.database.models.administrator import Administrator
from src.infrastructure.database.models.teacher import Teacher
from src.infrastructure.repositories.auth_repository.auth import add_user
from src.application.dto.auth.register_dto import RegisterDTO


async def add_in_teacher_or_admin(dto: RegisterDTO, hashed_password: str):
    data = dto.model_dump(exclude_none=True)
    data["password"] = hashed_password

    if dto.role == Role.TEACHER:
        user = Teacher(**data)
    else: 
        user = Administrator(**data)
    
    
    return await add_user(user)
        