from src.infrastructure.config.config import RESTORE_PASSWORD_LINK


def get_restore_password_link(restore_token: str) -> str:
    return RESTORE_PASSWORD_LINK.format(restore_token)
