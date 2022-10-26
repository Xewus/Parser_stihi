"""Сервер, принимающий запросы к `Scrapy`.
"""
from parser.helpers.enums import Tag
from parser.helpers.exceptions import NotFileException, ScrapyException
from parser.poems.commands import start_spider
from parser.settings import (APP_DESCRIPTION, APP_NAME, APP_VERSION, AUTHOR,
                             DEBUG, WEB_ALLOWED_HOSTS)
from parser.web.schemas import (ParsingArgsSchema, RespParsingArgsSchema,
                                RespTestSchema)
from parser.web.validators import app_key_validator

from fastapi import Body, FastAPI, Header
from fastapi.middleware.trustedhost import TrustedHostMiddleware

app = FastAPI(
    debug=DEBUG,
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    contact=AUTHOR
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=WEB_ALLOWED_HOSTS
)


@app.get(
    '/test',
    tags=[Tag.TEST],
    summary='Проверка доступности сервера',
    response_model=RespTestSchema
)
async def test_server(
    app_key=Header(
        description='Ключ доступа',
        example='SOME_KEY'
        )
) -> RespTestSchema:
    """Проверка доступности сервера.

    #### Args:
    - app_key (str): 'Ключ доступа'.

    #### Returns:
    - dict: Ответ сервера.
    """
    app_key_validator(app_key)
    return RespTestSchema(server='Ok')


@app.post(
    '/scrapy',
    tags=[Tag.SCRAPY],
    summary='Принимает параметры для запуска парсера',
    response_description='Путь к файлу с результатами парсинга',
    response_model=RespParsingArgsSchema
)
async def parse(
    app_key=Header(
        description='Ключ доступа',
        example='SOME_KEY'
    ),
    args: ParsingArgsSchema = Body(
        ..., examples=ParsingArgsSchema.Config.schema_extra['examples']
    )

) -> RespParsingArgsSchema:
    """Принимает параметры для запуска парсера'

    #### Args:
    - app_key (str): Ключ доступа.
    - args (json): json с аргументами.

    #### Raises:
    - NotFileException: Отсутствует ффйл с результатами.
    - ScrapyException: Проблемы при запуске `Scrapy`.

    #### Returns:
        RespParsingArgsSchema: URI файла с результатами.
    """
    app_key_validator(app_key)
    try:
        uri = await start_spider(**args.dict())
        return RespParsingArgsSchema(uri=uri)
    except FileNotFoundError as err:
        raise NotFileException(err.args)
    except Exception as exc:
        raise ScrapyException(exc.args)
