from bcrypt import gensalt, hashpw
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.infrastructure.config import config

Base = declarative_base()


def get_engine():
    return create_async_engine(config.DATABASE_URL, echo=True)


async def initialize_database(engine):
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

def get_session():
    engine = get_engine()
    return sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

async def run_database():
    engine = get_engine()
    await initialize_database(engine)