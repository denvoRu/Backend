from dataclasses import dataclass
from src.infrastructure.enums.role import Role


@dataclass
class User:
    username: str
    password: str