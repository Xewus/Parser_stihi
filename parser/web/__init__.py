"""API для доступа к `Scrapy`.
"""
from parser.db.models import create_first_user
from parser.settings import (APP_DESCRIPTION, APP_NAME, APP_VERSION, AUTHOR,
                             DEBUG, TORTOISE_CONFIG)

from parser.core.exceptions import BadRequestException
from fastapi import FastAPI, status
from tortoise.contrib.fastapi import register_tortoise
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
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

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    exc = exc.errors()[0]
    return JSONResponse(
        content=jsonable_encoder({'detail': '%s: %s' % (exc['loc'][1], exc['msg'])}),
        status_code=status.HTTP_400_BAD_REQUEST
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
