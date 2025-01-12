from src.infrastructure.config import config

from aiomodeus.selenium import auth as auth_modeus

def auth():
    return auth_modeus(
        config.MODEUS_LOGIN, 
        config.MODEUS_PASSWORD,
        config.SELENIUM_HUB_URL
    )