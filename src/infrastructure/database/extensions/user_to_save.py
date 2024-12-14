from typing import Union
from src.infrastructure.database.models.teacher import Teacher
from src.infrastructure.database.models.administrator import Administrator

def user_to_save_dict(user):
    return {
        "id": user.id,
        "first_name": user.first_name,
        "second_name": user.second_name,
        "third_name": user.third_name,
        "email": user.email
    }