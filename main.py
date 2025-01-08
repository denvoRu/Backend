from src.application import app
from src.infrastructure.config import config

import uvicorn


if __name__ == "__main__":
    # запуск сервер через uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=config.APP_PORT, 
        forwarded_allow_ips="*", 
        log_level="info"
    )
