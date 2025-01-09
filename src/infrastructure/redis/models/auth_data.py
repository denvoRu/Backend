from src.infrastructure.config import config
from src.infrastructure.enums.role import Role

from redis_om import JsonModel, Field
from uuid import UUID


class Users(JsonModel):
    id: UUID
    access_token: str = Field(index=True, full_text_search=True)
    refresh_token: str = Field(primary_key=True)
    role: Role

    class Meta:
        database = config.REDIS_CONN
