"""Сбор всех эндпоинтов в один.
"""
from fastapi import APIRouter

from app.enums import Tag
from . import users, parsing 



main_router = APIRouter()

default_router = APIRouter()


@default_router.get(
    path='/',
    tags=[Tag.INDEX],
    summary='Главная страница',
    description='Приветственная страница приложения.',
    response_description='Привествие и текст дальнейших действий.'
)
async def index_view():
    return {"message": "Hello World"}


@default_router.get('/wait')
async def wait_view():
    return {"message": "wait"}

main_router.include_router(
    router=default_router
)
main_router.include_router(
    router=parsing.router,
    prefix='/parsing',
    tags=[Tag.PARSING]
)
main_router.include_router(
    router=users.router,
    prefix='/users',
    tags=[Tag.USERS]
)
