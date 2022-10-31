"""Эндпоинты, не водшешие в другие роутеры.
"""
from parser.core.enums import Tag
from parser.web.schemas.parser_schemas import RespTestSchema

from fastapi import APIRouter

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
    '/test',
    tags=[Tag.TEST],
    summary='Проверка доступности сервера',
    response_model=RespTestSchema
)
async def test_server(
) -> RespTestSchema:
    """Проверка доступности сервера.
    """
    return RespTestSchema(server='Ok')
