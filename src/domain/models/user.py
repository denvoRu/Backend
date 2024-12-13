from dataclasses import dataclass
from src.domain.enums.role import Role


@dataclass
class User:
    username: str
    password: str