from src.infrastructure.database import db
from src.infrastructure.config import config
from src.application.controllers import api_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import Migrator


async def shutdown(app: FastAPI):
    db.init(config.DATABASE_URL)
    Migrator().run()
    await db.create_all()
    yield
    await db.close()


app = FastAPI(
    version=config.VERSION,
    title=config.PROJECT_NAME,
    summary=config.SUMMARY,
    lifespan=shutdown
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)
