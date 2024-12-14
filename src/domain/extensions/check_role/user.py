from src.domain.enums.role import Role
from dataclasses import dataclass

@dataclass
class User:
    username: str
    password: str
    role: Role