from src.infrastructure.enums.role import Role
from redis_om import JsonModel, Field

class Users(JsonModel):
    user_id: int
    access_token: str = Field(index=True, full_text_search=True)
    refresh_token: str = Field(primary_key=True)
    role: Role
