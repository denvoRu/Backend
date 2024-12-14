from src.domain.enums.role import Role
from src.infrastructure.redis import Users


def add_token_in_redis(username: str, role: Role, access_token: str, refresh_token: str) -> str:
    u = Users(
        username=username,
        role=role,
        access_token=access_token,
        refresh_token=refresh_token
    )
    u.save()
    return u.refresh_token