import uvicorn
from asyncio import run
from src.infrastructure.database import run_database
from src.application import app


if __name__ == "__main__":
    run(run_database())
    uvicorn.run(app, host="127.0.0.1", port=5000, log_level="info")