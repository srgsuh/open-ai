from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

async def request_validation_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=400,
            content={
                "detail": exc.errors()
            }
        )
    raise exc
     
async def response_validation_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        return JSONResponse(
            status_code=500,
            content={
                "detail": exc.errors()
            }
        )
    raise exc

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(RequestValidationError, response_validation_handler)