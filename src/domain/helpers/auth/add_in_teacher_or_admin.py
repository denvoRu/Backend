from domain.enums.role import Role
from infrastructure.database.models.administrator import Administrator
from infrastructure.database.models.teacher import Teacher
from infrastructure.repositories.auth_repository.auth import add_user
from src.application.dto.auth.register_dto import RegisterDTO

def add_in_teacher_or_admin(dto: RegisterDTO, hashed_password: str):
    instance = Teacher if dto.role == Role.TEACHER else Administrator
    user = instance(
        first_name=dto.first_name,
        second_name=dto.second_name,
        third_name=dto.third_name,
        email=dto.username,
        password=hashed_password
    )
    
    return add_user(user)
        