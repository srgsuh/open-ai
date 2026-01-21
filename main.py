from fastapi import FastAPI
from middleware import logging_mw
from routes.health import health_router
from routes.services import services_router
from exception_handlers import setup_exception_handlers

api_prefix: str = "/api"

app = FastAPI()

app.include_router(health_router)

app.include_router(services_router, prefix=api_prefix)

app.middleware("http")(logging_mw)

setup_exception_handlers(app)