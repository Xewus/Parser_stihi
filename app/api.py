from parser.poems.commands import start_spider

from fastapi import FastAPI, Header, Query
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from core.enums import SpiderNames
from core.validators import validate_author, validate_headers, validate_urls

app = FastAPI()

app.add_middleware(TrustedHostMiddleware, allowed_hosts=['127.0.0.1'])


@app.get('/test', summary='Test server availability')
def test() -> dict:
    return {'Server': 'OK'}


@app.get('/scrapy/{spider}')
async def parse(
    *,
    APP_KEY: str | None = Header(
        default=None,
        title='Ключ приложения',
        description='Ключ приложения имеющего допуск',
        example='qwerty'
    ),
    spider: SpiderNames,
    author: str = Query(
        title='Автор произведений',
        description='URL-ссылка на страницу автора.',
        examples={
            '1': {'value': 'oleg'},
            '2': {'value': 'https://stihi.ru/avtor/oleg'}
        }
    ),
    urls: str | None = Query(
        default=None,
        title='Список ссылок на стихи',
        description='Список URL-сыылок на стихи, для паука `choose-poems`'
    )
) -> dict:
    """Принимает команды для запуска парсеров.

    Example:
        http://127.0.0.1:5000/scrapy/all-poems&author=oleg

    Returns:
        str: _description_
    """
    ok, message = validate_headers('APP_KEY', APP_KEY)
    if not ok:
        return {'error': message, 'status': 403}

    author, message = await validate_author(author)
    if not author:
        return {'error': message, 'status': 400}

    if spider == SpiderNames.CHOOSE_POEMS:
        urls = validate_urls(urls)
        if not urls:
            return {'error': 'Wrong urls', 'status': 400}

    await start_spider(spider, author, urls)
    return {'file': "ok"}


@app.get('/scrapy/{spider}', tags=['Inside'])
async def send_command(
    *,
    APP_KEY: str | None = Header(
        default=None,
        title='Ключ приложения',
        description='Ключ приложения имеющего допуск',
        example='qwerty'
    ),
    spider: SpiderNames,
    author: str = Query(
        title='Автор произведений',
        description='URL-ссылка на страницу автора.',
        examples={
            '1': {'value': 'oleg'},
            '2': {'value': 'https://stihi.ru/avtor/oleg'}
        }
    ),
    urls: str | None = Query(
        default=None,
        title='Список ссылок на стихи',
        description='Список URL-сыылок на стихи, для паука `choose-poems`'
    )
) -> dict:
    """Вызывает команды для запуска парсеров.
    Принимает запросы только с разрешёнными API_KEY.

    Example:
        http://127.0.0.1:5000/scrapy/all-poems&author=oleg

    Returns:
        str: _description_
    """
    ok, message = validate_headers('APP_KEY', APP_KEY)
    if not ok:
        return {'error': message, 'status': 403}
    await start_spider(spider, author, urls)
    return {'file': "ok"}


@app.get('/parsing/{spider}')
async def parse(
    *,
    spider: SpiderNames,
    author: str = Query(
        title='Автор произведений',
        description='URL-ссылка на страницу автора.',
        examples={
            '1': {'value': 'oleg'},
            '2': {'value': 'https://stihi.ru/avtor/oleg'}
        }
    ),
    urls: str | None = Query(
        default=None,
        title='Список ссылок на стихи',
        description='Список URL-сыылок на стихи, для паука `choose-poems`'
    )
) -> dict:
    """Принимает команды для запуска парсеров.

    Example:
        http://127.0.0.1:5000/scrapy/all-poems&author=oleg

    Returns:
        str: _description_
    """
    author, message = await validate_author(author)
    if not author:
        return {'error': message, 'status': 400}

    if urls:
        urls = validate_urls(urls)

    await start_spider(spider, author, urls)

    if spider == SpiderNames.CHOOSE_POEMS:
        if not urls:
            return {'error': 'Wrong urls', 'status': 400}
    return {'file': "ok"}