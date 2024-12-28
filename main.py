from src.application import app

import uvicorn


if __name__ == "__main__":
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=5000, 
        forwarded_allow_ips="*", 
        log_level="info"
    )
