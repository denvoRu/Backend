from src.infrastructure.database import db
from src.infrastructure.config import config
from src.application.controllers import api_router

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import Migrator


async def shutdown(app: FastAPI):
    db.init(config.DATABASE_URL)
    await db.create_all()
    Migrator().run()
    yield
    await db.close()


app = FastAPI(
    version=config.VERSION,
    title=config.PROJECT_NAME,
    summary=config.SUMMARY,
    lifespan=shutdown,
    root_path=config.ROOT_PATH
)  # main app creation logic with config information

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=1728000
)  # add a cors middleware from FastAPI to an app

app.include_router(api_router)  # add a main router to an app that includes all routers from /controllers
