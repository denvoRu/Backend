from fastapi.security import OAuth2PasswordRequestForm
from domain.enums.role import Role


class ExtendedOAuth2PasswordRequestForm(OAuth2PasswordRequestForm):
    role: Role