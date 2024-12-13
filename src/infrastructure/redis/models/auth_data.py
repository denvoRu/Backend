from src.domain.enums.role import Role
from redis_om import HashModel, Field

class Users(HashModel):
    access_token: str = Field(primary_key=True)
    username: str
    role: Role