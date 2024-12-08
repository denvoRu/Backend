from decouple import config
from sqlalchemy import URL

PROJECT_NAME = config("PROJECT_NAME")
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
