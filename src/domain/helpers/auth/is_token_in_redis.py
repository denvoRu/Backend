from src.infrastructure.redis import Users


def is_token_in_redis(refresh_token: str) -> bool:
    """
    Checks that token is in Redis
    """
    try:
        Users.get(refresh_token)
        return True
    except Exception:
        return False
        