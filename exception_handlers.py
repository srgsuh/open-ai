from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from logs import logger

async def request_validation_handler(request: Request, exc: Exception) -> JSONResponse:    
    logger.debug(f"Catch ERROR: {str(exc)}, type={type(exc)}")
    if isinstance(exc, RequestValidationError):
        logger.debug(f"MATCH ERROR TYPE RESPONSE WITH")
        return JSONResponse(
            status_code=400,
            content={
                "detail": jsonable_encoder(exc.errors())
            }
        )
    raise exc
     
async def response_validation_handler(request: Request, exc: Exception) -> JSONResponse:
    if isinstance(exc, ValidationError):
        return JSONResponse(
            status_code=500,
            content={
                "detail": jsonable_encoder(exc.errors())
            }
        )
    raise exc

def setup_exception_handlers(app: FastAPI):
    app.add_exception_handler(RequestValidationError, request_validation_handler)
    app.add_exception_handler(ValidationError, response_validation_handler)