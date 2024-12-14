from src.infrastructure.enums.role import Role
from dataclasses import dataclass

@dataclass
class User:
    user_id: int
    username: str
    password: str
    role: Role