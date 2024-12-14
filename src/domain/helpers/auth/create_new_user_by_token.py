from src.domain.extensions.token import create_token
from src.domain.models.user import User
from src.infrastructure.redis import Users


def create_new_user_by_token(refresh_token: str) -> str:
    c = Users.get(refresh_token)
    new_token = create_token(
        User(c.username, ''),
        c.role
    )
    new_user = Users(
        access_token=new_token.access_token,
        refresh_token=new_token.refresh_token,
        username=c.username,
        role=c.role
    )
    c.delete(refresh_token)
    new_user.save()
    
    return new_token