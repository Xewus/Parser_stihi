"""API для доступа к `Scrapy`.
"""
from parser.db.user_models import create_first_user
from parser.settings import (APP_DESCRIPTION, APP_NAME, APP_VERSION, AUTHOR,
                             DEBUG)

from fastapi import FastAPI

from .routers.default_router import router as default_router
from .routers.parsing import router as parsing_router
from .routers.users import router as users_router

app = FastAPI(
    debug=DEBUG,
    title=APP_NAME,
    version=APP_VERSION,
    description=APP_DESCRIPTION,
    contact=AUTHOR
)

app.include_router(default_router)
app.include_router(parsing_router)
app.include_router(users_router)


@app.on_event('startup')
async def startup():
    create_first_user()
