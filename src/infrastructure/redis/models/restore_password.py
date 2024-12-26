from src.infrastructure.config.config import REDIS_DATABASE_CONN
from src.infrastructure.enums.role import Role

from redis_om import JsonModel, Field


class RestorePassword(JsonModel):
    restore_token: str = Field(primary_key=True)
    email: str
    role: Role

    class Meta:
        database = REDIS_DATABASE_CONN
