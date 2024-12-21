from src.infrastructure.redis import RestorePassword


def get_restore_token_from_redis(restore_token: str) -> RestorePassword:
    return RestorePassword.get(restore_token)
