import uuid


def get_hex_uuid():
    return uuid.uuid4().hex  # creates an uuid for our models/tables
