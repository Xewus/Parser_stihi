from parser.poems.commands import start_spider
from parser.poems.helpers.enums import SpiderNames
from parser.poems.helpers.validators import validate_headers, validate_author, validate_urls

import requests
from fastapi import FastAPI, Header, Query, Depends

app = FastAPI()

async def common_parameters(q: str | None = None, skip: int = 0, limit: int = 100):
    return {"q": q, "skip": skip, "limit": limit}



@app.get(
    path='/test',
    summary='Test server availability')
def test(
    commons: dict = Depends(common_parameters)
) -> dict:
    return commons# {'Server': 'OK'}


@app.get('/scrapy/{spider}')
async def parse(*,
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
            '1': {'value': 'mazurrussia'},
            '2': {'value': 'https://stihi.ru/avtor/mazurrussia'}
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
        http://127.0.0.1:5000/scrapy/all-poems&author=ivanov

    Returns:
        str: _description_
    """
    ok, message = await validate_headers('APP_KEY', APP_KEY)
    if not ok:
        return {'error': message, 'status': 403}

    author, message = await validate_author(author)
    if not author:
        return {'error': message, 'status': 400}

    if spider == SpiderNames.CHOOSE_POEMS:
        urls = validate_urls(urls)
        if not urls:
            return {'error': 'Wrong urls', 'status': 400}
        values = (author, urls)
    else:
        values = (author,)

    await start_spider(spider, values)
    return {'auyhor': author, 'spider': spider}
