"""Сервер, принимающий запросы к `Scrapy`.
"""
import json
from parser.poems.commands import start_spider

from aiohttp import web
from aiohttp.web_request import Request
from aiohttp.web_response import Response

from core import constants as cnst
from core.settings import HEADERS, WEB_SCRAPY_HOST, WEB_SCRAPY_PORT


def check_app_key(request: Request) -> bool:
    """Проверяет разрешение по заголовку.

    #### Args:
    - request (Request): Объект запроса.

    #### Returns:
    - bool: Пройдена ли проверка.
    """
    return request.headers.get(cnst.APP_KEY) == HEADERS[cnst.APP_KEY]


async def test_server(request: Request) -> Response:
    """Эндпоинт для проверки доступности сервера.

    #### Args:
    - request (Request): Объект запроса.

    #### Returns:
    - Response: Объект ответа
    """
    data = {cnst.SERVER_SCRAPY: cnst.OK}
    if not check_app_key(request):
        data[cnst.SERVER_SCRAPY] = cnst.APP_KEY
    return web.json_response(data)



async def parse(request: Request):
    text = await request.text()
    args = {}
    for arg in text.split('&'):
        key, value = arg.split('=')
        if value == 'None':
            value = None
        args[key] = value
    await start_spider(**args)
    return web.json_response({'parsed': 'ok'})

app = web.Application()
app.add_routes([
    web.get('/test', test_server),
    web.post('/scrapy', parse)
])

set_app = {'app': app, 'host': WEB_SCRAPY_HOST, 'port': WEB_SCRAPY_PORT}
