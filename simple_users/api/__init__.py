"""Эндпоинты для приложения `simple_users`.
"""
from fastapi import FastAPI

from simple_users.db.models import create_first_user

from .router import router as users_router

app = FastAPI(
    debug=1,
    title='SimpleUsers',
    version='0.1.0'
)

app.include_router(
    router=users_router,
    prefix='/users'
)


@app.on_event('startup')
async def startup():
    create_first_user()
