from decouple import config
from sqlalchemy import URL
from redis_om import get_redis_connection

from src.infrastructure.helpers.get_semestr_end_date import (
    get_semester_end_date
)


REDIS_CONN = get_redis_connection(url=config("REDIS_OM_URL"))

PROJECT_NAME = config("PROJECT_NAME")
APP_PORT = config("APP_PORT", cast=int)
VERSION = "1.0.0"
SUMMARY = "Web applications for collecting statistics on the work of teachers at the institute for future analysis"

RESTORE_PASSWORD_TOKEN_EXPIRE_SECONDS = 60 * 60 * 2
RESTORE_PASSWORD_LINK: str = config("RESTORE_PASSWORD_LINK")

REGISTERED_HTML = "" 
UPDATE_PASSWORD_HTML = ""

ALGORITHM = "HS256"
JWT_SECRET_KEY = config("JWT_SECRET_KEY")

DATABASE_CONFIG = {
    "drivername": config("DATABASE_DRIVER_NAME"),
    "host": config("DATABASE_HOST"),
    "port": config("DATABASE_PORT"),
    "username": config("DATABASE_USERNAME"),
    "password": config("DATABASE_PASSWORD"),
    "database": config("DATABASE"),
}
DATABASE_URL = URL.create(**DATABASE_CONFIG)

MAIL_FROM = config("MAIL_FROM")
MAIL_SERVER = config("MAIL_SERVER")
MAIL_PORT = config("MAIL_PORT")
MAIL_USERNAME = config("MAIL_USERNAME")
MAIL_PASSWORD = config("MAIL_PASSWORD")

ROOT_PATH = "/api/v1"

MODEUS_LOGIN = config("MODEUS_LOGIN")
MODEUS_PASSWORD = config("MODEUS_PASSWORD")

SELENIUM_HUB_URL= config("SELENIUM_HUB_URL")

END_OF_SEMESTR = get_semester_end_date()