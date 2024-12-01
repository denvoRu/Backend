import asyncio

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.app.config import config
from src.app.api.router import api_router
from src.database.initialize_database import run_database

app = FastAPI(
    title=config.PROJECT_NAME,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(api_router)

if __name__ == "__main__":
    asyncio.run(run_database())
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")
