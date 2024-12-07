from decouple import config
from sqlalchemy import URL

PROJECT_NAME = config("PROJECT_NAME")
DATABASE = {
    "drivername": config("DATABASE_DRIVER_NAME"),
    "host": config("DATABASE_HOST"),
    "port": config("DATABASE_PORT"),
    "username": config("DATABASE_USERNAME"),
    "password": config("DATABASE_PASSWORD"),
    "database": config("DATABASE"),
    "plugins": config("DATABASE_PLUGINS"),
}
DATABASE_URL = URL.create(DATABASE["plugins"], username=DATABASE["username"], password=DATABASE["password"],
                          host=DATABASE["host"], port=DATABASE["port"], database=DATABASE["database"])

ALGORITHM = "HS256"
JWT_SECRET_KEY = config("JWT_SECRET_KEY")
