from src.infrastructure.database import (
    get, Administrator
)
from typing import List


async def get_by_email(email: str,) -> dict:
    return await get.get_by_email(email, Administrator)
    
async def all() -> List[dict]:
    return await get.get_all(Administrator)
    