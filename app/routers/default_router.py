"""Сбор всех эндпоинтов в один.
"""
from fastapi import APIRouter
import json

from app.core.enums import Tag
from app.core import constants as cnst
from app.core.requests import SendRequest
from app.core.settings import WEB_SCRAPY_URL, HEADERS
from app.schemas import RespTestSchema

router = APIRouter()


@router.get(
    path='/',
    tags=[Tag.INDEX],
    summary='Главная страница',
    description='Приветственная страница приложения.',
    response_description='Привествие и текст дальнейших действий.'
)
async def index_view():
    return {"message": "Hello World.\nПривествие и текст дальнейших действий"}


@router.get(
    path='/test',
    tags=[Tag.DEFAULT],
    summary='Проверяет доступность серверов.',
    response_model=RespTestSchema
)
async def test() -> dict:
    data = {
        cnst.SERVER_WEB: cnst.OK,
        cnst.SERVER_SCRAPY: cnst.NOT_OK
        }
    request = SendRequest(url=WEB_SCRAPY_URL + 'test', headers=HEADERS)
    response = await request.GET
    match response:
        case None:
            ...
        case _:
            data = data | json.loads(await response.text())

    return data


# @drouter.get('/wait')
# async def wait_view():
#     return {"message": "wait"}

# main_router.include_router(
#     router=default_router
# )
# main_router.include_router(
#     router=parsing.router,
#     prefix='/parsing',
#     tags=[Tag.PARSING]
# )
# main_router.include_router(
#     router=users.router,
#     prefix='/users',
#     tags=[Tag.USERS]
# )
