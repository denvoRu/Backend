from src.infrastructure.database.extensions.initial_sql import INITIAL_SQL

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel, text


class AsyncDatabaseSession:
    def __init__(self):
        self.session = None
        self.engine = None


    def __getattr__(self, name):
        return getattr(self.session, name)


    def init(self, url: str):
        self.engine = create_async_engine(url, future=True, echo=True,pool_size=10, max_overflow=20)
        self.session = sessionmaker(self.engine, expire_on_commit=False, class_=AsyncSession)()


    async def create_all(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)

        for query in INITIAL_SQL:
            try:   
                await db.execute(text(query))
            except Exception: pass
            finally:
                await self.commit_rollback()


    async def commit_rollback(self):
        try:
            await self.commit()
        except Exception:
            await self.rollback()
            raise


db = AsyncDatabaseSession()
