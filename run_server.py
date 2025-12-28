import uvicorn
from configuration import get_config_parameter
from logs import logger

DEFAULT_PORT: int = 8000

port: int = int(get_config_parameter("PORT", "8000"))

if __name__ == "__main__":
    port: int = int(get_config_parameter("PORT", "8000"))
    logger.debug(f"Running a server on a port {port}")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        workers=4,
        log_level="info"
    )