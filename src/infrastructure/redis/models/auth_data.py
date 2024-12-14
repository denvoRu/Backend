from src.infrastructure.enums.role import Role
from redis_om import JsonModel, Field, Migrator

class Users(JsonModel):
    access_token: str = Field(index=True, full_text_search=True)
    refresh_token: str = Field(primary_key=True)
    username: str
    role: Role

Migrator().run()