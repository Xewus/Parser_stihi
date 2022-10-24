import json

from fastapi import FastAPI, Query

from core import constants as cnst
from core.enums import SpiderNames
from core.settings import HEADERS, WEB_SCRAPY_URL
from core.utils import SendRequest
from core.validators import validate_author, validate_urls

app = FastAPI()


@app.get('/test', summary='Проверяет доступность серверов.')
async def test() -> dict:
    data = {
        cnst.SERVER_WEB: cnst.OK,
        cnst.SERVER_SCRAPY: cnst.NOT_OK
        }
    request = SendRequest(url=WEB_SCRAPY_URL + 'test', headers=HEADERS)
    response = await request.GET
    if response and response.ok:
        data = data | json.loads(await response.text())

    return data


@app.get('/parsing/{spider}')
async def parse(
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

    if spider == SpiderNames.CHOOSE_POEMS:
        urls = validate_urls(urls)
        if not urls:
            return {'error': 'Wrong urls', 'status': 400}

    scrapy_url = WEB_SCRAPY_URL + 'scrapy'
    payload = {
        'spider': spider,
        'author': author,
        'urls': urls
    }
    request = SendRequest(url=scrapy_url, data=payload)
    response = await request.POST
    print(response)
    text = await response.text()
    return text


# @app.get('/scrapy/{spider}', tags=['Inside'])
# async def send_command(
#     *,
#     APP_KEY: str | None = Header(
#         default=None,
#         title='Ключ приложения',
#         description='Ключ приложения имеющего допуск',
#         example='qwerty'
#     ),
#     spider: SpiderNames,
#     author: str = Query(
#         title='Автор произведений',
#         description='URL-ссылка на страницу автора.',
#         examples={
#             '1': {'value': 'oleg'},
#             '2': {'value': 'https://stihi.ru/avtor/oleg'}
#         }
#     ),
#     urls: str | None = Query(
#         default=None,
#         title='Список ссылок на стихи',
#         description='Список URL-сыылок на стихи, для паука `choose-poems`'
#     )
# ) -> dict:
#     """Вызывает команды для запуска парсеров.
#     Принимает запросы только с разрешёнными API_KEY.

#     Example:
#         http://127.0.0.1:5000/scrapy/all-poems&author=oleg

#     Returns:
#         str: _description_
#     """
#     ok, message = validate_headers('APP_KEY', APP_KEY)
#     if not ok:
#         return {'error': message, 'status': 403}
#     await start_spider(spider, author, urls)
#     return {'file': "ok"}


# @app.get('/parsing/{spider}')
# async def parse(
#     *,
#     spider: SpiderNames,
#     author: str = Query(
#         title='Автор произведений',
#         description='URL-ссылка на страницу автора.',
#         examples={
#             '1': {'value': 'oleg'},
#             '2': {'value': 'https://stihi.ru/avtor/oleg'}
#         }
#     ),
#     urls: str | None = Query(
#         default=None,
#         title='Список ссылок на стихи',
#         description='Список URL-сыылок на стихи, для паука `choose-poems`'
#     )
# ) -> dict:
#     """Принимает команды для запуска парсеров.

#     Example:
#         http://127.0.0.1:5000/scrapy/all-poems&author=oleg

#     Returns:
#         str: _description_
#     """
#     author, message = await validate_author(author)
#     if not author:
#         return {'error': message, 'status': 400}

#     if urls:
#         urls = validate_urls(urls)

#     await start_spider(spider, author, urls)

#     if spider == SpiderNames.CHOOSE_POEMS:
#         if not urls:
#             return {'error': 'Wrong urls', 'status': 400}
#     return {'file': "ok"}
