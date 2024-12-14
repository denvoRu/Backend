from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker
from src.infrastructure.config import config
from sqlmodel import SQLModel


def get_engine():
    return create_async_engine(config.DATABASE_URL, echo=True)


async def initialize_database(engine):
    async with engine.begin() as conn:
        await SQLModel.metadata.create_all(engine)

def get_session():
    engine = get_engine()
    return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def run_database():
    engine = get_engine()
    await initialize_database(engine)