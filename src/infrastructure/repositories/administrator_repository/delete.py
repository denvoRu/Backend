from src.infrastructure.database import get_session, Administrator
from sqlalchemy import delete

async def delete_admin(admin_id: int):
    async_session = get_session()

    async with async_session() as session:
        stmt = delete(Administrator).where(Administrator.id == admin_id)
        await session.execute(stmt)
        await session.commit()
        