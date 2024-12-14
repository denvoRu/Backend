from dataclasses import dataclass
from src.infrastructure.enums.role import Role


@dataclass
class User:
    user_id: int
    password: str