from sqlalchemy import delete
from src.infrastructure.database.initialize_database import get_session


async def delete_user(admin_id: int, instance):
    async_session = get_session()

    async with async_session() as session:
        stmt = delete(instance).where(instance.id == admin_id)
        await session.execute(stmt)
        await session.commit()