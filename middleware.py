from typing import Awaitable, Callable
from fastapi import Request, Response
from logs import logger

async def logging_mw(request: Request, call_next: Callable[[Request], Awaitable[Response]]) -> Response:
    logger.info("request. method: %s, path: %s, port: %s", request.method, request.url.path, request.url.port)
    response: Response = await call_next(request)
    logger.info("response. status: %s", response.status_code)
    return response