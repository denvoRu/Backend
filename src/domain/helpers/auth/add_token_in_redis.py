from src.infrastructure.enums.role import Role
from src.infrastructure.redis import Users

from uuid import UUID


def add_token_in_redis(id: UUID, role: Role, access_token: str, refresh_token: str) -> str:
    """
    Refreshes token in Redis
    """
    u = Users(
        id=id,
        role=role,
        access_token=access_token,
        refresh_token=refresh_token
    )
    u.save()
    return u.refresh_token