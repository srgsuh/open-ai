from fastapi import FastAPI
from middleware import logging_mw
from routes.travel import travel_router

app = FastAPI()

app.include_router(travel_router, prefix="/travel")

app.middleware("http")(logging_mw)

