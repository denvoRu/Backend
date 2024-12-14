from src.infrastructure.enums.role import Role
from src.infrastructure.database.models.administrator import Administrator
from src.infrastructure.database.models.teacher import Teacher
from src.infrastructure.repositories.auth_repository.auth import add_user
from src.application.dto.auth.register_dto import RegisterDTO

async def add_in_teacher_or_admin(dto: RegisterDTO, hashed_password: str):
    instance = Teacher if dto.role == Role.TEACHER else Administrator
    user = instance(
        first_name=dto.first_name,
        second_name=dto.second_name,
        third_name=dto.third_name,
        email=dto.username,
        password=hashed_password
    )
    
    return await add_user(user)
        