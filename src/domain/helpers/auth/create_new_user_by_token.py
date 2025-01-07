from src.domain.extensions.token import create_token
from src.infrastructure.redis import Users


def create_new_user_by_token(refresh_token: str) -> str:
    """
    Creates new tokens for a user
    """
    c = Users.get(refresh_token)
    new_token = create_token(c.id, c.role)
    new_user = Users(
        access_token=new_token.access_token,
        refresh_token=new_token.refresh_token,
        id=c.id,
        role=c.role
    )
    c.delete(refresh_token)
    new_user.save()
    
    return new_token
