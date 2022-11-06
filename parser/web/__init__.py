"""API для доступа к `Scrapy`.
"""
from parser.db.models import create_first_user
from parser.settings import (APP_DESCRIPTION, APP_NAME, APP_VERSION, AUTHOR,
                             DEBUG, TORTOISE_CONFIG)

from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

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

app.include_router(
    router=default_router
)
app.include_router(
    router=users_router,
    prefix='/users'
)
app.include_router(
    router=parsing_router
)

register_tortoise(
    app=app,
    **TORTOISE_CONFIG
)


@app.on_event('startup')
async def startup():
    await create_first_user()
