from fastapi import FastAPI
from middleware import logging_mw
from routes.travel import travel_router
from routes.health import health_router
from routes.services import services_router
from exception_handlers import setup_exception_handlers

app = FastAPI()

#Health-checking route
app.include_router(health_router, prefix="/health")
#Applicational routes
app.include_router(services_router, prefix="/api")
app.include_router(travel_router, prefix="/api/travel")

app.middleware("http")(logging_mw)

setup_exception_handlers(app)