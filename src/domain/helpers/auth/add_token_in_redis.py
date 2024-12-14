from src.infrastructure.enums.role import Role
from src.infrastructure.redis import Users


def add_token_in_redis(user_id: int, role: Role, access_token: str, refresh_token: str) -> str:
    u = Users(
        user_id=user_id,
        role=role,
        access_token=access_token,
        refresh_token=refresh_token
    )
    u.save()
    return u.refresh_token