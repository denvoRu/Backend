from src.infrastructure.enums.role import Role

from uuid import UUID
from dataclasses import dataclass


@dataclass
class User:
    user_id: UUID
    username: str
    password: str
    role: Role