from decouple import config
from sqlalchemy import URL
from redis_om import get_redis_connection


PROJECT_NAME = config("PROJECT_NAME")
VERSION = "1.0.0"
SUMMARY = "Web applications for collecting statistics on the work of teachers at the institute for future analysis"

RESTORE_PASSWORD_TOKEN_EXPIRE_SECONDS = 60 * 60 * 2
RESTORE_PASSWORD_LINK = config("RESTORE_PASSWORD_LINK")

REGISTERED_HTML = '' 
UPDATE_PASSWORD_HTML = ''

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

REDIS_CONFIG = {
    "host": config("REDIS_HOST"),
    "port": config("REDIS_PORT"),
    "username": config("REDIS_USERNAME"),
    "password": config("REDIS_PASSWORD"),
}
url = f'redis://{REDIS_CONFIG["username"]}:{REDIS_CONFIG["password"]}@{REDIS_CONFIG["host"]}:{REDIS_CONFIG["port"]}/'
REDIS_DATABASE_CONN = get_redis_connection(url=url)

MAIL_FROM = config("MAIL_FROM")
MAIL_SERVER = config("MAIL_SERVER")
MAIL_PORT = config("MAIL_PORT")
MAIL_USERNAME = config("MAIL_USERNAME")
MAIL_PASSWORD = config("MAIL_PASSWORD")
