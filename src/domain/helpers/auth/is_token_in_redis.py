from src.infrastructure.redis import Users

def is_token_in_redis(token: str) -> bool:
    return Users.get(token) is not None