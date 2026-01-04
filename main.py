from fastapi import FastAPI
from middleware import logging_mw
from routes.travel import travel_router
from routes.health import health_router
from exception_handlers import setup_exception_handlers

app = FastAPI()

app.include_router(travel_router, prefix="/travel")
app.include_router(health_router, prefix="/health")

app.middleware("http")(logging_mw)

setup_exception_handlers(app)