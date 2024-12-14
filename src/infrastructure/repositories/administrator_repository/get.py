from .models import admin_to_save_dict
from src.infrastructure.database import (
    get, Administrator
)
from typing import List


async def get_by_email(email: str,) -> dict:
    admin = await get.get_by_email(email, Administrator)
    return admin_to_save_dict(admin)
    
async def all() -> List[dict]:
    data = await get.get_all(Administrator)
    save_data = [admin_to_save_dict(admin) for admin in data]
    return list(save_data)
