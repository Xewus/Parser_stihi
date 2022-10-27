"""Сбор всех эндпоинтов в один.
"""
from parser.core.enums import Tag
from parser.web.schemas import RespTestSchema

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
