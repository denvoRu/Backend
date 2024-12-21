from src.infrastructure.config.config import RESTORE_PASSWORD_TOKEN_EXPIRE_SECONDS
from src.infrastructure.redis import RestorePassword
from src.infrastructure.enums.role import Role


def add_restore_data_in_redis(
        email: str, role: Role, restore_token: str
) -> RestorePassword:
    rp = RestorePassword(
        email=email,
        role=role,
        restore_token=restore_token
    )
    rp.expire(RESTORE_PASSWORD_TOKEN_EXPIRE_SECONDS)
    rp.save()
