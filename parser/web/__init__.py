"""API для запуска `Scrapy`.
"""
from parser.settings import (APP_DESCRIPTION, APP_NAME, APP_VERSION, AUTHOR,
                             DEBUG)

from fastapi import FastAPI

from .routers.default_router import router as default_router
from .routers.parsing import router as parsing_router

app = FastAPI(
    debug=DEBUG,
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    contact=AUTHOR
)

app.include_router(default_router)
app.include_router(parsing_router)
