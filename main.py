from fastapi import FastAPI
from middleware import logging_mw

app = FastAPI()

app.middleware("http")(logging_mw)

