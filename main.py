from fastapi import FastAPI
from middleware import logging_mw
from routes.travel import travel_router
from auth import auth_router
from exception_handlers import setup_exception_handlers

app = FastAPI()

app.include_router(travel_router, prefix="/travel")
app.include_router(auth_router, prefix="/auth")

app.middleware("http")(logging_mw)

setup_exception_handlers(app)