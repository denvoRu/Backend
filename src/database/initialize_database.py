from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.app.config import config

Base = declarative_base()


def get_engine():
    return create_async_engine(config.DATABASE_URL, echo=True)


async def initialize_database(engine):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)


async def run_database():
    engine = get_engine()
    await initialize_database(engine)
    async_session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        async with session.begin():
            ...
        result = await session.execute(text("SELECT 1"))